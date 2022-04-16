FROM ubuntu:20.04

RUN apt-get update && apt-get install python3 python3-pip -y 

COPY . /Docker

WORKDIR ./Docker

RUN pip3 install -r requirements.txt

RUN pip3 install tensorflow==2.8 --no-cache-dir

CMD ['python3', 'main.py']