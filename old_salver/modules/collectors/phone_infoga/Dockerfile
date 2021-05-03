FROM golang:1.16.0-buster as build-env


RUN curl -sSL https://raw.githubusercontent.com/sundowndev/PhoneInfoga/master/support/scripts/install | bash \
    && mv phoneinfoga /go/bin


ENTRYPOINT ["phoneinfoga"]
