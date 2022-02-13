FROM python:3.7-buster

WORKDIR /sherlock-master

RUN curl -fL -o /tmp/master.zip https://github.com/sherlock-project/sherlock/archive/master.zip  \
    && unzip /tmp/master.zip -d / \
    && cd /sherlock-master && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "/sherlock-master/sherlock/sherlock.py"]