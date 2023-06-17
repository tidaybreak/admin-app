IDE Debug Parameters:runserver -h 0.0.0.0 -p 8004

python manage.py rsync_catalog
python manage.py rsync_schema
python manage.py rsync_entity -s schema
python manage.py fix_data -l 10
python manage.py fix_data -s switch -l 10
                                                
删缓存
redis-cli  -n 1 keys "dcim_cache:*" | xargs redis-cli -n 1 del

Flask 将数据库表转换为sqlalchemy models
pip install sqlacodegen
sqlacodegen mysql+pymysql://root:ti999@172.18.0.5/dcim > app/models/sqlacodegen.py

### greenlet
On Python 3.7, you either need gevent >= 1.4.0, < 20.9; greenlet >= 0.4.14, < 0.4.17 OR gevent >= 20.9; greenlet >= 0.4.17.
On Python 3.8 or 3.9, the minimum gevent version is 20.6.0, and the minimum greenlet version is 0.4.16.
I'd just use gevent>= 20.9; greenlet >= 0.4.17 everywhere.

screen      
source env/bin/activate             
export C_FORCE_ROOT="true"
export PYTHONUNBUFFERED=1
export APP_CONFIG=Env               
export APP_NAME=dcim
gunicorn -k gevent -t 120 -b "0.0.0.0:8004" -w 1 --capture-output --log-file=/tmp/dcim-app.log manage:app &
celery -A manage.celery worker --beat --loglevel=info               
tail -f /tmp/dcim-app.log                                               


docker run -ti --rm harbor.ofidc.com/public/python:3.6.9-alpine-20200614 /bin/sh
docker commit -a "ti" -m "why" 0437b0c35978 harbor.ofidc.com/public/python:3.6.9-alpine-20200619
docker push harbor.ofidc.com/public/python:3.6.9-alpine-20200619


docker build -t admin-app:v1 .  --network host \
--build-arg HTTP_PROXY=http://wengzt%40ofidc.com:ti2751231@proxy.tiham.com:1090 \
--build-arg HTTPS_PROXY=http://wengzt%40ofidc.com:ti2751231@proxy.tiham.com:1090 \


docker stop admin-app
docker rm admin-app
docker run --name admin-app -d \
--hostname admin-app \
--net mynet \
--ip 172.18.0.112 \
-e PYTHONUNBUFFERED=1 \
-e APP_CONFIG=Env \
-e TERM=linux \
-e C_FORCE_ROOT=true \
-e APP_NAME=admin \
-e SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:ti999@mysql-dev.ofidc.com:3306/admin?charset=utf8 \
-e REDIS_URL=redis://redis-dev.ofidc.com:6379/1' \
-e CACHE_REDIS_URL=redis://redis-dev.ofidc.com:6379/1' \
-e CELERY_BROKER_URL=redis://redis-dev.ofidc.com:6379/5 \
-e CELERY_RESULT_BACKEND=redis://redis-dev.ofidc.com:6379/5 \
--mount type=bind,source=/etc/resolv.docker.conf,target=/etc/resolv.conf \
--mount type=bind,source=/data/logs/,target=/wls/logs \
--mount type=bind,source=/home/data/docker-volume/admin-app/,target=/app \
admin-app:v1     /app/run.sh