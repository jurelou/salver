FROM python:3.7-buster

WORKDIR /zen

RUN git clone --depth 1 --branch v1.1 https://github.com/s0md3v/Zen.git /zen \
	&& cd /zen \
	&& pip3 install -r requirements.txt

ENTRYPOINT [ "python", "zen.py" ]