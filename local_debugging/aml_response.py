from flask import Response
import json


class AMLResponse(Response):
    def __init__(self, message, status_code, response_headers={}, json_str=True, run_function_failed=False):
        if message is not None:
            if json_str:
                super().__init__(json.dumps(message), status=status_code, mimetype='application/json')
            else:
                super().__init__(message, status=status_code)
        else:
            # return empty json if message is None
            super().__init__(json.dumps({}), status=status_code, mimetype='application/json')

        self.headers['x-ms-run-function-failed'] = run_function_failed

        # If the user run() want to response repeated headers, comma should be used as the seperator
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2
        for header, value in response_headers.items():
            for v in value.split(","):
                self.headers.add_header(header, v.strip())

