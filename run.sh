#!/bin/sh

export log_dir=./logs
export now_time=`date +%Y-%m-%d-%H-%M-%S`

export C_FORCE_ROOT=true
export APP_CONFIG=Env

cd /app/

python generate_config.py
supervisord -c supervisord.conf
