FROM python:3.8-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/salver

COPY ./setup.py .
COPY ./salver ./salver
COPY ./Makefile ./Makefile

RUN pip install --upgrade pip setuptools wheel && \
    pip install . --use-feature=in-tree-build


ENTRYPOINT [ "python" ]