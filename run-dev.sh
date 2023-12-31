#!/bin/sh

rm -rf ./celerybeat.pid
rm -rf ./supervisor.sock
rm -rf ./celerybeat-schedule
rm -rf /tmp/admin-log
mkdir -p /tmp/admin-log
export log_dir=/tmp/admin-log
export now_time=`date +%Y-%m-%d-%H-%M-%S`
export C_FORCE_ROOT=true
export PYTHONUNBUFFERED=1
export APP_CONFIG=Env

python generate_config.py
supervisord -c supervisord.conf
