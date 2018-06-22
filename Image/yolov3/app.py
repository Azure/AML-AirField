import flask
import traceback
import json
import signal
from aml_blueprint import AMLBlueprint
from aml_response  import AMLResponse
from flask import request
from werkzeug.http import parse_options_header
from run_function_exception import RunFunctionException
from timeout_exception import TimeoutException

from azureml.api.exceptions.ClientSideException import ClientSideException
from azureml.api.exceptions.ServerSideException import ServerSideException

import main as real_main

main = AMLBlueprint('main', __name__)

# Health probe endpoint
@main.route('/', methods=['GET'])
def health_probe():
    return "Healthy"

@main.route('/ui', methods=['GET'])
def html_ui():
    resp = flask.send_file('ui.html', add_etags=False)
    resp.headers['Content-Encoding'] = 'identity'
    return resp

@main.route('/score', methods=['POST'])
def score_realtime():
    flask.g.apiName = "/score"

    # run the user-provided run function
    return run_scoring(lambda: real_main.run(request))

# Errors from Server Side
@main.errorhandler(ServerSideException)
def handle_exception(error):
    main.logger.debug("Server side exception caught")
    main.stop_hooks()
    main.logger.error("Encountered Exception: {0}".format(traceback.format_exc()))
    return AMLResponse(error.to_dict(), error.status_code)


# Errors from Client Request
@main.errorhandler(ClientSideException)
def handle_exception(error):
    main.logger.debug("Client request exception caught")
    main.stop_hooks()
    main.logger.error("Encountered Exception: {0}".format(traceback.format_exc()))
    return AMLResponse(error.to_dict(), error.status_code)


# Errors from User Run Function
@main.errorhandler(RunFunctionException)
def handle_exception(error):
    main.logger.debug("Run function exception caught")
    main.stop_hooks()
    main.logger.error("Encountered Exception: {0}".format(traceback.format_exc()))
    return AMLResponse(error.message, error.status_code, json_str=False, run_function_failed=True)


# Errors of Scoring Timeout
@main.errorhandler(TimeoutException)
def handle_exception(error):
    main.logger.debug("Run function timeout caught")
    main.stop_hooks()
    main.logger.error("Encountered Exception: {0}".format(traceback.format_exc()))
    return AMLResponse(error.message, error.status_code, json_str=False, run_function_failed=True)


# Unhandled Error
# catch all unhandled exceptions here and return the stack encountered in the response body
@main.errorhandler(Exception)
def unhandled_exception(error):
    main.stop_hooks()
    main.logger.debug("Unhandled exception generated")
    error_message = "Encountered Exception: {0}".format(traceback.format_exc())
    main.logger.error(error_message)
    internal_error = "An unexpected internal error occurred. {0}".format(error_message)
    return AMLResponse(internal_error, 500, json_str=False)


# log all response status code after request is done
@main.after_request
def after_request(response):
    if getattr(flask.g, 'apiName', None):
        main.logger.info(response.status_code)
    return response

def run_scoring(user_func):
    main.start_hooks(request.environ.get('REQUEST_ID', '00000000-0000-0000-0000-000000000000'))

    try:
        response = invoke_user_with_timer(user_func)
    except ClientSideException:
        raise
    except ServerSideException:
        raise
    except TimeoutException:
        main.stop_hooks()
        main.send_exception_to_app_insights(request)
        raise
    except Exception as exc:
        main.stop_hooks()
        main.send_exception_to_app_insights(request)
        raise RunFunctionException(str(exc))
    finally:
        main.stop_hooks()

    if isinstance(response, flask.Response):
        return response
    else:
        return AMLResponse(response, 200)

def alarm_handler(signum, frame):
    error_message = "Scoring timeout after {} ms".format(main.scoring_timeout_in_ms)
    raise TimeoutException(error_message)

def invoke_user_with_timer(user_func):
    old_handler = signal.signal(signal.SIGALRM, alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, main.scoring_timeout_in_ms / 1000)
    main.logger.info("Scoring Timer is set to {} seconds".format(main.scoring_timeout_in_ms / 1000))

    result = user_func()

    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.signal(signal.SIGALRM, old_handler)

    return result
