import os
import sys
#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
bind = '127.0.0.1:9090'

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
workers = 1
timeout = int(os.environ.get("WORKER_TIMEOUT", 120))

#
# Logging Configuration
# log-config - the config file which tels gunicorn how to log

logconfig = "gunicorn_logging.conf"

#
# Server hooks
# worker_abort - called when a worker received the SIGABRT signal
#   pre_fork - Called just prior to forking the worker subprocess.
#


def pre_fork(server, worker):
    server.log.info("worker timeout is set to {0}".format(timeout))


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
    sys.exit(3)


def worker_abort(worker):
    worker.log.error("worker timed out, killing gunicorn")
    sys.exit(3)

