FROM python:3

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt 

FROM ubuntu:18.04

RUN apt -y update && apt install -y libsm6
RUN apt install -y libxrender1
RUN apt install -y libfontconfig1
RUN apt install -y libice6
