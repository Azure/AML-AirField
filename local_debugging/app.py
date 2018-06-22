import flask
import traceback
import json
import signal
from aml_blueprint import AMLBlueprint
from aml_response  import AMLResponse
from flask import request
import main as user_main
from werkzeug.http import parse_options_header
from run_function_exception import RunFunctionException
from timeout_exception import TimeoutException

try:
    from azureml.api.exceptions.ClientSideException import ClientSideException
except ImportError:
    from azure.ml.api.exceptions.ClientSideException import ClientSideException

try:
    from azureml.api.exceptions.ServerSideException import ServerSideException
except ImportError:
    from azure.ml.api.exceptions.ServerSideException import ServerSideException

main = AMLBlueprint('main', __name__)

@main.route('/score', methods=['GET'])
def get_prediction_realtime():
    flask.g.apiName = "/prediction"

    # Some Notes:
    #   - Request arg keys are case-sensitive(RFC 3986)
    #   - If there are repeated arg in the url, its values will be put as an array in the request body
    #
    # For example:
    #   - GET http://127.0.0.1:9090/score?foo=bar1&Foo=bar2&x=y
    #     * run() will receive
    #         {
    #             "Foo": "bar2",
    #             "foo": "bar1",
    #             "x": "y"
    #         }
    #   - GET http://127.0.0.1:9090/score?foo=bar1&foo=bar2&x=y
    #     * run() will receive
    #         {
    #             "x": "y",
    #             "foo": [
    #                 "bar1",
    #                 "bar2"
    #             ]
    #         }

    aml_input = {}
    for k in request.args.keys():
        values = request.args.getlist(k)
        if len(values) == 1:
            aml_input[k] = json.loads(values[0]) if is_json(values[0]) else values[0]
        else:
            value_list = []
            for v in values:
                value_list.append(json.loads(v) if is_json(v) else v)

            aml_input[k] = value_list

    # run the user-provided run function
    return run_scoring(json.dumps(aml_input), request.headers)


@main.route('/score', methods=['POST'])
def score_realtime():
    flask.g.apiName = "/score"

    # always enforce content-type json as either the sdk or the user code is expected to json deserialize this
    main.logger.info("Validation Request Content-Type")
    if 'Content-Type' not in request.headers or parse_options_header(request.headers['Content-Type'])[0] != 'application/json':
        return AMLResponse({"message": "Expects Content-Type to be application/json"}, 415)

    # always expects the response to be utf-8 encodeable
    service_input = request.data.decode("utf-8")

    # run the user-provided run function
    return run_scoring(service_input, request.headers)


@main.route('/swagger.json', methods=['GET'])
def get_swagger_specification():
    flask.g.apiName = "/swagger.json"
    if main.swagger:
        return AMLResponse(main.swagger, 200)
    main.logger.info("Swagger file not present")
    return AMLResponse("Swagger not found", 404)


# Health probe endpoint
@main.route('/', methods=['GET'])
def health_probe():
    return "Healthy"


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


def run_scoring(service_input, request_headers):
    main.logger.info("Received input: {0}".format(service_input))
    main.logger.info("Headers passed in (total {0}):".format(len(request_headers)))
    for k, v in request_headers.items():
        main.logger.info("\t{0}: {1}".format(k, v))

    main.start_hooks(request.environ.get('REQUEST_ID', '00000000-0000-0000-0000-000000000000'))

    try:
        response = invoke_user_with_timer(service_input, request_headers)
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

    response_headers = {}
    response_body = response
    response_status_code = 200

    if isinstance(response, dict):
        if 'aml_response_headers' in response:
            main.logger.info("aml_response_headers are available from run() output")
            response_body = None
            response_headers = response['aml_response_headers']

        if 'aml_response_body' in response:
            main.logger.info("aml_response_body is available from run() output")
            response_body = response['aml_response_body']

    return AMLResponse(response_body, response_status_code, response_headers)


def alarm_handler(signum, frame):
    error_message = "Scoring timeout after {} ms".format(main.scoring_timeout_in_ms)
    raise TimeoutException(error_message)


def invoke_user_with_timer(input, headers):
    params = {main.run_input_parameter_name: input}

    # Flask request.headers is not python dict but werkzeug.datastructures.EnvironHeaders which is not json serializable
    # Per RFC 2616 sec 4.2,
    # 1. HTTP headers are case-insensitive: https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2
    #    So if user scores with header ("foo": "bar") from client, but what we give run() function could be ("FOO": "bar")
    # 2. HTTP header key could be duplicate. In this case, request_headers[key] will be a list of values.
    #    Values are connected by ", ". For example a request contains "FOO": "bAr" and "foO": "raB",
    #    the request_headers["Foo"] = "bAr, raB".

    if main.support_request_header:
        params["request_headers"] = dict(headers)

    old_handler = signal.signal(signal.SIGALRM, alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, main.scoring_timeout_in_ms / 1000)
    main.logger.info("Scoring Timer is set to {} seconds".format(main.scoring_timeout_in_ms / 1000))

    result = user_main.run(**params)

    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.signal(signal.SIGALRM, old_handler)

    return result


def is_json(input_string):
    try:
        json_object = json.loads(input_string)
    except ValueError:
        return False
    return True
