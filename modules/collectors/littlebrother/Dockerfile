FROM python:3.6-buster

WORKDIR /LittleBrother

RUN git clone --depth 1 https://github.com/lulz3xploit/LittleBrother.git /LittleBrother \
	&& cd /LittleBrother \
	&& pip3 install -r requirements.txt

COPY entrypoint.sh /LittleBrother/entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
