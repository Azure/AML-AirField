import json
import os
import sys
import inspect
import traceback

sys.path.append('/var/azureml-app/')
from flask import Blueprint
from appinsights import AppInsightsClient, WSGIWrapper
from aml_logger import AMLLogger
import main
from print_hook import PrintHook
from wsgi_request import WSGIRequest


class AMLBlueprint(Blueprint):
    appinsights_client = None
    stdout_hook = None
    stderr_hook = None
    appinsights_enabled = None
    swagger = False
    swagger_spec_path = './swagger.json'
    support_request_header = False
    run_input_parameter_name = 'input'
    scoring_timeout_env_variable = 'SCORING_TIMEOUT_MS'
    scoring_timeout_in_ms = 3600 * 1000
    logger = None

    # init wsgi wrapper that handles request Id generation
    def _init_request_id_generator(self, app):
        try:
            self.logger.info("Starting up request id generator")
            app.wsgi_app = WSGIRequest(app.wsgi_app)
        except:
            self.logger.error(
                "Encountered exception while starting up request_id generator: {0}".format(traceback.format_exc()))
            sys.exit(3)

    def _init_logger(self):
        try:
            print("Initializing logger")
            self.logger = AMLLogger()
        except:
            print("logger initialization failed: {0}".format(traceback.format_exc()))
            sys.exit(3)

    def _get_swaggger(self):
        if os.path.exists(self.swagger_spec_path):
            with open(self.swagger_spec_path, 'r') as file:
                data = json.load(file)
                return data
        return None

    # AML App Insights WSGI Wrapper
    def _init_appinsights(self, app):
        try:
            self.logger.info("Starting up app insights client")
            self.appinsights_client = AppInsightsClient()
            app.wsgi_app = WSGIWrapper(app.wsgi_app, self.appinsights_client)
            self.stdout_hook = PrintHook(PrintHook.stdout_fd)
            self.stderr_hook = PrintHook(PrintHook.stderr_fd)
        except:
            self.logger.error(
                "Encountered exception while initializing App Insights/Logger {0}".format(traceback.format_exc()))
            sys.exit(3)

    def send_exception_to_app_insights(self, request):
        if self.appinsights_client is not None:
            self.appinsights_client.send_exception_log(sys.exc_info(), request.environ.get('REQUEST_ID', 'NoRequestId'))

    def start_hooks(self, prefix='no request id'):
        try:
            if self.stdout_hook is not None:
                self.stdout_hook.start_hook(prefix)
            if self.stderr_hook is not None:
                self.stderr_hook.start_hook(prefix)
        except:
            pass

    def stop_hooks(self):
        try:
            if self.stdout_hook is not None:
                self.stdout_hook.stop_hook()
            if self.stderr_hook is not None:
                self.stderr_hook.stop_hook()
        except:
            pass

    def register(self, app, options, first_registration=False):

        # initiliaze request generator, logger and app insights
        self._init_logger()
        self._init_appinsights(app)
        self._init_request_id_generator(app)

        # start the hooks to listen to init print events
        try:
            self.logger.info("Starting up app insight hooks")
            self.start_hooks()
        except:
            self.logger.error("Starting up app insight hooks failed")
            if self.appinsights_client is not None:
                self.appinsights_client.send_exception_log(sys.exc_info())
            sys.exit(3)

        # actually get init started
        try:
            self.logger.info("Invoking user's init function")
            main.init()
            self.logger.info("Users's init has completed successfully")
        except:
            self.logger.error("User's init function failed")
            self.logger.error("Encountered Exception {0}".format(traceback.format_exc()))
            if self.appinsights_client is not None:
                self.appinsights_client.send_exception_log(sys.exc_info())
            sys.exit(3)
        finally:
            self.stop_hooks()

        # set has_swagger value
        self.swagger = self._get_swaggger()

        # check if run() support handling request header
        run_args = inspect.signature(main.run).parameters.keys()
        run_args_list = list(run_args)
        if len(run_args) > 2:
            self.logger.error("run() has too many parameters")
            sys.exit(3)

        if len(run_args) == 2 and 'request_headers' not in run_args:
            self.logger.error("run() has 2 parameters, but request_headers is not found")
            sys.exit(3)

        if len(run_args) == 1:
            self.support_request_header = False
            self.run_input_parameter_name = run_args_list[0]
        else:
            self.support_request_header = True
            self.run_input_parameter_name = run_args_list[0] if run_args_list[0] != "request_headers" else run_args_list[1]

        if self.scoring_timeout_env_variable in os.environ.keys() and \
                self.is_int(os.environ[self.scoring_timeout_env_variable]):
            self.scoring_timeout_in_ms = int(os.environ[self.scoring_timeout_env_variable])
            self.logger.info("Scoring timeout is found from os.environ: {} ms".format(self.scoring_timeout_in_ms))
        else:
            self.logger.info("Scoring timeout setting is not found. Use default timeout: {} ms".format(self.scoring_timeout_in_ms))

        super(AMLBlueprint, self).register(app, options, first_registration)

    def is_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False