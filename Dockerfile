FROM python:3.7-slim
MAINTAINER Yaroslav <hello@unimarijo.com>
ENV INSTALL_PATH /data

COPY . $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -y sysbench fio wget gcc
RUN pip install -r requirements.txt

CMD python benchmarks.py
