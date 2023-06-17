[supervisord]
user=root
nodaemon=true
directory=%(here)s
logfile=%(ENV_log_dir)s/supervisord-%(ENV_now_time)s.log

{% if SUPERVISOR_HTTP_SERVER_ENABLE -%}
[inet_http_server]
port={{SUPERVISOR_HTTP_SERVER_PORT}}
{% if SUPERVISOR_BASIC_AUTH_ENABLE -%}
username={{SUPERVISOR_BASIC_AUTH_USERNAME}}
password={{SUPERVISOR_BASIC_AUTH_PASSWORD}}
{%- endif %}
{%- endif %}

{% if SUPERVISOR_UNIX_SOCKS_PATH -%}
[unix_http_server]
file={{SUPERVISOR_UNIX_SOCKS_PATH}}
{%- endif %}

{% if SUPERVISOR_UNIX_SOCKS_PATH -%}
[supervisorctl]
serverurl=unix://{{SUPERVISOR_UNIX_SOCKS_PATH}}
{%- endif %}

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[program:app]
command=gunicorn -k gevent -t 120 -b "0.0.0.0:8000" -w 4 manage:app
autostart=true
startretries=3
redirect_stderr=true
stdout_logfile=%(ENV_log_dir)s/admin-%(ENV_now_time)s.log
stdout_logfile_backups=0

[program:celery]
command=celery -A manage.celery worker --loglevel=info
autostart=true
startretries=3
redirect_stderr=true
stdout_logfile=%(ENV_log_dir)s/celery-%(ENV_now_time)s.log
stdout_logfile_backups=0

[program:celery_beat]
command=celery -A manage.celery beat
autostart=true
startretries=3
redirect_stderr=true
stdout_logfile=%(ENV_log_dir)s/beat-%(ENV_now_time)s.log
stdout_logfile_backups=0

[program:flower]
command=flower -A manage.celery --port=8001 --url_prefix=api/v1/celery --persistent=True {% if FLOWER_BASIC_AUTH_ENABLE %}--basic_auth={{FLOWER_BASIC_AUTH_USERNAME}}:{{FLOWER_BASIC_AUTH_PASSWORD}}{% endif %}
autostart=true
startretries=3
redirect_stderr=true
stdout_logfile=%(ENV_log_dir)s/flower-%(ENV_now_time)s.log
stdout_logfile_backups=0