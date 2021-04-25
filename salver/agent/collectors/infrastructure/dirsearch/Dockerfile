FROM python:3.7-buster


WORKDIR /dirsearch-0.4.1/

RUN curl -fL -o /tmp/v0.4.1.zip https://github.com/maurosoria/dirsearch/archive/v0.4.1.zip \
    && unzip /tmp/v0.4.1.zip -d / \
    && cd /dirsearch-0.4.1/ && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "/dirsearch-0.4.1/dirsearch.py"]
