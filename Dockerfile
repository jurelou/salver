FROM python:3.8-buster

WORKDIR /opt/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools wheel
COPY ./setup.py .
RUN pip install .[api]

COPY ./salver ./salver

ENTRYPOINT ["uvicorn", "salver.api.main:app", "--host", "0.0.0.0", "--reload"]
