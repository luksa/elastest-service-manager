FROM gliderlabs/alpine:latest

LABEL maintainer "elastest-users@googlegroups.com"
LABEL version="0.1.0"
LABEL description="Builds the service manager docker image."

WORKDIR /app

COPY . /app

RUN apk --update add --virtual build-dependencies \
    python3-dev \
    build-base \
    curl \
    && pip3 install --upgrade pip \
    && pip3 install virtualenv \
    && virtualenv /env \
    && /env/bin/pip3 install -r /app/requirements.txt

# endpoint of the EPM
# ENV EPM_SVC_EP http://somewhere.io:4533/epm

# port on which the ESM runs
ENV ESM_PORT 8080

EXPOSE 8080

CMD ["/env/bin/python", "/app/runesm.py"]
