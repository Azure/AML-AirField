import datetime
import re

class WSGIWrapper(object):
    def __init__(self, inner_app, app_insights_client):
        if not inner_app:
            raise Exception('WSGI application was required but not provided')
        if not app_insights_client:
            raise Exception('App Insights Client was required but not provided')
        self._inner_app = inner_app
        self.appinsights_client = app_insights_client

    def __call__(self, environ, start_response):
        request_path = environ.get('PATH_INFO') or '/'
        start_time = datetime.datetime.utcnow()

        closure = {'status': '200 OK'}
        response_value = ''
        
        def response_interceptor(status_string, headers_array, exc_info=None):
            closure['status'] = status_string
            start_response(status_string, headers_array, exc_info)

        for data in self._inner_app(environ, response_interceptor):
            response_value = data or ''
            yield data

        success = True
        response_match = re.match(r'\s*(?P<code>\d+)', closure['status'])
        if response_match:
            response_code = response_match.group('code')
            if int(response_code) >= 400:
                success = False
        else:
            response_code = closure['status']
            success = False

        http_method = environ.get('REQUEST_METHOD', 'GET')
        url = request_path
        query_string = environ.get('QUERY_STRING')
        if query_string:
            url += '?' + query_string

        scheme = environ.get('wsgi.url_scheme', 'http')
        host = environ.get('HTTP_HOST', environ.get('SERVER_NAME', 'unknown'))

        url = scheme + '://' + host + url

        end_time = datetime.datetime.utcnow()
        duration = int((end_time - start_time).total_seconds() * 1000)

        request_id = environ.get('REQUEST_ID', '00000000-0000-0000-0000-000000000000')
        if request_path != '/':
            self.appinsights_client.send_request_log(request_id, response_value, request_path, url, success, start_time.isoformat() + 'Z', duration, response_code, http_method)
