FROM python:3.7-buster


WORKDIR /recon-ng-5.1.1

RUN curl -fL -o /tmp/v5.1.1.zip https://github.com/lanmaster53/recon-ng/archive/v5.1.1.zip \
    && unzip /tmp/v5.1.1.zip -d / \
    && cd /recon-ng-5.1.1 && pip install --no-cache-dir -r REQUIREMENTS \
    && echo "marketplace install all\nexit" | /recon-ng-5.1.1/recon-ng

ENTRYPOINT ["python", "/recon-ng-5.1.1/recon-cli"]