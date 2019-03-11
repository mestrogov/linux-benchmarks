FROM ubuntu:bionic
MAINTAINER Yaroslav <hello@unimarijo.com>
ENV INSTALL_PATH /data

COPY . $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -y python3 python3-pip sysbench fio wget
RUN pip3 install -r requirements.txt

CMD python3 benchmarks.py
