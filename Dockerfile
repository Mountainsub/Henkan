FROM python

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt 

FROM python

RUN apt -y update && apt install -y libsm6
RUN apt install -y libxrender1
RUN apt install -y libfontconfig1
RUN apt install -y libice6