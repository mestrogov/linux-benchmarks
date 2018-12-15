#!/bin/bash

echo "### Updating system packages ..."
apt update && apt -y upgrade

echo "### Installing needed packages ..."
apt install -y python3 python3-pip sysbench fio speedtest-cli wget
pip3 install psutil

python3 benchmarks.py