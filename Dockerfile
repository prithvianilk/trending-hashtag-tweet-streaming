FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y tmux default-jdk scala wget vim software-properties-common python3.8 python3-pip curl unzip libpq-dev build-essential libssl-dev libffi-dev python3-dev&& \
    apt-get clean

RUN wget https://archive.apache.org/dist/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz && \
    tar xvf spark-3.0.1-bin-hadoop3.2.tgz && \
    mv spark-3.0.1-bin-hadoop3.2/ /opt/spark && \
    wget https://archive.apache.org/dist/kafka/1.1.0/kafka_2.11-1.1.0.tgz && \
    tar -xzf kafka_2.11-1.1.0.tgz && \
    mv kafka_2.11-1.1.0 /opt/kafka && \
    ln -s /usr/local/spark spark

RUN curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y mongodb-org

RUN wget https://downloads.mongodb.com/compass/mongosh-1.3.1-linux-arm64.tgz && \
    tar -zxvf mongosh-1.3.1-linux-arm64.tgz && \
    chmod +x mongosh-1.3.1-linux-arm64/bin/mongosh && \
    chmod +x mongosh-1.3.1-linux-arm64/bin/mongocryptd-mongosh && \
    cp mongosh-1.3.1-linux-arm64/bin/mongosh /usr/local/bin && \
    cp mongosh-1.3.1-linux-arm64/bin/mongocryptd-mongosh /usr/local/bin && \
    mkdir -p /var/lib/mongo && \
    mkdir -p /var/log/mongodb && \
    chown `whoami` /var/lib/mongo && \
    chown `whoami` /var/log/mongodb

RUN pip3 install cython==0.29.21 numpy==1.18.5 && pip3 install tweepy pytest pyspark pandas==1.0.5 requests requests-oauthlib kafka-python pymongo

WORKDIR app
COPY . /app
ENV PYSPARK_PYTHON=python3
