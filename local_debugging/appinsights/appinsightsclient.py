import os
import json
import traceback
import applicationinsights as appinsights

class AppInsightsClient(object):
    """Batching parameters, whichever of the below conditions gets hit first will trigger a send.
        send_interval: interval in seconds
        send_buffer_size: max number of items to batch before sending
    """
    send_interval = 5.0
    send_buffer_size = 100

    def __init__(self):
        self.enabled = False
        if os.getenv('AML_APP_INSIGHTS_ENABLED') == 'true' and 'AML_APP_INSIGHTS_KEY' in os.environ:
            instrumentation_key = os.getenv('AML_APP_INSIGHTS_KEY')
            exception_channel = self._make_telemetry_channel()
            self.telemetry_client = appinsights.TelemetryClient(instrumentation_key, exception_channel)
            self._request_channel = self._make_telemetry_channel()
            self._container_id = os.getenv('HOSTNAME', 'Unknown')
            self.enabled = True

    def send_request_log(self, request_id, response_value, name, url, success, start_time, duration, response_code, http_method):
        try:
            if not self.enabled:
                return
            data = appinsights.channel.contracts.RequestData()
            data.id = request_id
            data.name = name
            data.start_time = start_time
            data.duration = self._calc_duration(duration)
            
            data.response_code = response_code
            data.success = success
            data.http_method = http_method
            data.url = url
            
            data.properties = { 'Container Id': self._container_id, 'Response Value': json.dumps(response_value.decode('utf-8')) }

            self._request_channel.write(data, self.telemetry_client.context)
        except:
            pass

    def send_exception_log(self, exc_info, request_id='Unknown'):
        try:
            if not self.enabled:
                return
            properties_dict = { 'Container Id': self._container_id, 'Request Id': request_id }
            self.telemetry_client.track_exception(*exc_info, properties=properties_dict)
        except:
            pass

    def _make_telemetry_channel(self):
        sender = appinsights.channel.AsynchronousSender()
        sender.send_interval = AppInsightsClient.send_interval
        sender.send_buffer_size = AppInsightsClient.send_buffer_size
        queue = appinsights.channel.AsynchronousQueue(sender)
        telemetry_channel = appinsights.channel.TelemetryChannel(None, queue)
        return telemetry_channel

    def _calc_duration(self, duration):
        local_duration = duration or 0
        duration_parts = []
        for multiplier in [1000, 60, 60, 24]:
            duration_parts.append(local_duration % multiplier)
            local_duration //= multiplier
        duration_parts.reverse()
        formatted_duration = '%02d:%02d:%02d.%03d' % tuple(duration_parts)
        if local_duration:
            formatted_duration = '%d.%s' % (local_duration, formatted_duration)
        return formatted_duration

