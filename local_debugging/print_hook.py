import syslog
import sys
import json
import datetime

""" PrintHook intercepts stdout/stderr output, appends a comma-separated prefix, sends the
    modified message with a prefix to syslog through either the syslog facilities LOG_LOCAL1 
    or LOG_LOCAL2 and sends the unmodified message back to its original destination (stdout/stderr)
    To begin the intercept, start_hook() method must explicitly be called after initialization.
    The same instance may be reused to start and stop the hook multiple times.
    Based off example from : https://code.activestate.com/recipes/579132-print-hook/
    Usage:
        from print_hook import PrintHook
        ph = PrintHook(PrintHook.stdout_fd)
        print('Hello World)     # Hello World
        ph.start_hook('My Prefix')
        print('Hello World')    # My Prefix, Hello World
        ph.stop_hook()          # Hello World
"""
class PrintHook(object):
    # Class variables to represent which of stdout/stderr to enable hooks for
    stdout_fd = 1
    stderr_fd = 2
    """ Initializes the stdout/err hook. Initializing it alone will not begin intercepting
        stdout/stderr. start_hook must be called to begin the intercept and redirection.
        
        Members:
            _facility:
                syslog.LOG_LOCAL1 and syslog.LOG_LOCAL2 correspond to the syslog facilities
                that can be used for identifying and filtering specific messages in syslog.
                LOG_LOCAL0 to LOG_LOCAL7 are facilities available for local use cases. 
                Others, such as LOG_KERN, LOG_USER are reserved for specific use cases: 
                i.e. LOG_KERN for kernel related logs. This class uses LOG_LOCAL1 for stdout 
                and LOG_LOCAL2 for stderr redirection.
            _prefix:
                default prefix is set to no request id as it may not always be called within
                a request's lifecycle.
            _target_fd: 
                stores information on whether stdout or stderr is intercepted. See class variables
                stdout_fd and stderr_fd
            _original_fd:
                keep a handle to the original stdout and stderr so the unparsed message can be
                passed to the original file descriptors.
    """
    def __init__(self, file_descriptor=1):
        self._original_fd = None
        self._target_fd = file_descriptor
        self._facility = syslog.LOG_LOCAL1 if file_descriptor==PrintHook.stdout_fd else syslog.LOG_LOCAL2
        self._prefix = '00000000-0000-0000-0000-000000000000'
        self._started = False

    def start_hook(self, prefix='00000000-0000-0000-0000-000000000000'):
        if not self._started:
            self.set_prefix(prefix)
            if self._target_fd == PrintHook.stdout_fd:
                self._original_fd = sys.stdout
                sys.stdout = self
            else:
                self._original_fd = sys.stderr
                sys.stderr = self
            self._started = True

    def stop_hook(self):
        if self._started:
            self._original_fd.flush()
            if self._target_fd == PrintHook.stdout_fd:
                sys.stdout = self._original_fd
            else:
                sys.stderr = self._original_fd
            self._started = False
    
    def set_prefix(self, prefix):
        self._prefix = prefix

    def write(self, text):
        if len(text.rstrip()):
            console_text = text.rstrip() + "\n"
            syslog_text = self._prefix + "," + console_text
            self._pipe_to_original_dest(console_text)
            self._pipe_as_logger(text)
            self._pipe_to_syslog(syslog_text)
    
    def _pipe_to_original_dest(self, console_text):
        self._original_fd.write(console_text)
    
    def _pipe_as_logger(self, text):
        json_msg = {'logger': 'logger_stdout' if self._target_fd == PrintHook.stdout_fd else 'logger_stderr',
                    'request_id':self._prefix,
                    'message': text,
                    'timestamp': datetime.datetime.now().isoformat()}
        self._original_fd.write(json.dumps(json_msg)+ "\n")

    def _pipe_to_syslog(self, syslog_text):
        syslog.syslog(self._facility, syslog_text)
    
    # pass any unhandled methods to original fd
    def __getattr__(self, name):
        return self._original_fd.__getattribute__(name)

