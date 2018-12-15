FROM ubuntu:latest


MAINTAINER Yaroslav <hello@unimarijo.com>

COPY run.sh data data/
WORKDIR data

CMD ["bash", "run.sh"]