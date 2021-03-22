FROM python:3.8-buster

WORKDIR /opt/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools wheel
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]