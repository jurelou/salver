FROM python:3.6-buster

WORKDIR /BlackWidow



RUN git clone --depth 1 --branch v1.3 https://github.com/1N3/BlackWidow.git /BlackWidow \
	&& cd /BlackWidow \
	&& pip3 install -r requirements.txt \
	&& mv injectx.py /usr/bin/injectx.py


ENTRYPOINT [ "python", "/BlackWidow/blackwidow" ]
