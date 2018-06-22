class TimeoutException(Exception):
    status_code = 500

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
