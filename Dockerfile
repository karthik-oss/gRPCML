#FROM python:3.7-alpine as base
#FROM python:3.5-alpine as base
FROM python:3.8-slim as base

ENV http_proxy 'http://10.117.168.149:9005'
ENV https_proxy 'http://10.117.168.149:9005'
ENV HTTP_PROXY 'http://10.117.168.149:9005'
ENV HTTPS_PROXY 'http://10.117.168.149:9005'
WORKDIR .
EXPOSE 9090
ENTRYPOINT ["python3", "epg_ad_server.py"]

ADD requirements.txt .
##RUN apk update && \
RUN apt-get update
RUN apt-get install --yes net-tools procps
RUN apt-get install --yes  python3 python3-pip gcc gfortran python3 python3-dev libpng-dev libfreetype6 libfreetype6-dev freetype2-demos pkg-config
RUN pip3 install setuptools
RUN pip3 install wheel
#RUN pip3 install freetype
#RUN pip3 install  matplotlib
RUN pip3 install numpy==1.17.2
RUN pip3 install scipy
#RUN pip3 install --no-cache-dir  numpy
#RUN pip3 install --no-cache-dir  statsmodels
##RUN  apt-get install -y python3 python-pip && \
RUN pip3 install -r requirements.txt


COPY * ./

#RUN  python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
