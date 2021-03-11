FROM python:3.7-buster

WORKDIR /theHarvester-3.2.3

RUN curl -fL -o /tmp/master.zip https://github.com/laramies/theHarvester/archive/3.2.3.zip  \
    && unzip /tmp/master.zip -d / \
    && cd /theHarvester-3.2.3 && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "theHarvester.py"]