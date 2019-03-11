FROM python:3.6-alpine
RUN mkdir /usr/src/osp
WORKDIR /usr/src/osp
COPY requirements.txt .
RUN pip install -r requirements.txt
