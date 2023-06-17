#!/bin/sh

export log_dir=/wls/logs
export now_time=`date +%Y-%m-%d-%H-%M-%S`

cd /app/

python generate_config.py
supervisord -c supervisord.conf
