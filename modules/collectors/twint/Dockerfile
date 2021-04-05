FROM python:3.6-buster

WORKDIR /twint

RUN git clone --depth=1 https://github.com/twintproject/twint.git /twint \
	&& cd /twint \
	&& pip3 install . -r requirements.txt

ENTRYPOINT [ "twint" ]
