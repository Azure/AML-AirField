import flask
import json
import logging
from flask import request


class AMLLogger:
    def __init__(self):
        #initializing logger
        self.logger = logging.getLogger("root")
        self.logger.setLevel(logging.INFO)

    def _get_request_id(self):
        empty_guid = '00000000-0000-0000-0000-000000000000'
        if flask.has_request_context() and hasattr(request, 'environ'):
            return request.environ.get('REQUEST_ID', empty_guid)
        else:
            return empty_guid

    def _get_api_name(self):
        default = ''
        if flask.has_request_context() and getattr(flask.g, 'apiName', None):
            return flask.g.apiName
        else:
            return default

    def _get_record(self, message):
        data_obj = dict()
        data_obj["requestId"] = self._get_request_id()
        data_obj["message"] = message
        data_obj["apiName"] = self._get_api_name()
        return data_obj

    def call_log(self, message, func):
        record = self._get_record(message)
        func(json.dumps(record))

    def debug(self, message):
        self.call_log(message, self.logger.debug)

    def info(self, message):
        self.call_log(message, self.logger.info)

    def error(self, message):
        self.call_log(message, self.logger.error)

    def critical(self, message):
        self.call_log(message, self.logger.critical)

