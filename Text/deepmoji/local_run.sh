set -e

source activate deepmojienv

gunicorn -c gunicorn_conf.py "wsgi:app" | jq -R -r '. as $line | try (fromjson | .message, .exc_info) catch $line'
