FROM python:3.6-buster

WORKDIR /kupa3

RUN git clone --depth 1 https://github.com/woj-ciech/kupa3.git /kupa3 \
	&& cd /kupa3 \
	&& pip3 install -r requirements.txt

ENTRYPOINT [ "python", "kupa3.py" ]
