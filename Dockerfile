FROM python:3.6.8-alpine

WORKDIR /app

#RUN addgroup -S app && adduser -S -G app app

RUN pip install --upgrade pip
RUN sed -i 's/https/http/' /etc/apk/repositories
RUN apk --no-cache add gcc musl-dev libffi libffi-dev
RUN mv /usr/local/lib/python3.6/site-packages /app
RUN ln -s /app/site-packages /usr/local/lib/python3.6/site-packages

#USER app



COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/run.sh"]


#FROM harbor.ofidc.com/public/python:3.6.9-alpine-200221025
#ADD ./dcim-app.tar.gz /wls/applications/
#ADD ./run.sh /run.sh
#RUN chmod +x /run.sh
#RUN mkdir -p /wls/logs /wls/applications/
#ENV LANG en_US.UTF-8
#ENV RES_OPTIONS "timeout:1 attempts:1 ndots:2"
#WORKDIR /wls/applications/dcim-app
#EXPOSE 8000 8001 9001
#CMD ["/run.sh"]
