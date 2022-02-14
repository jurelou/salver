FROM python:3.7-buster

WORKDIR /Infoga-master

RUN curl -fL -o /tmp/master.zip https://github.com/m4ll0k/Infoga/archive/master.zip  \
    && unzip /tmp/master.zip -d / \
    && cd /Infoga-master && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "infoga.py"]