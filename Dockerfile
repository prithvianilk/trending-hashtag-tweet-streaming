FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y tmux default-jdk scala wget vim software-properties-common python3.8 python3-pip curl unzip libpq-dev build-essential libssl-dev libffi-dev python3-dev&& \
    apt-get clean

RUN wget https://archive.apache.org/dist/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz && \
    tar xvf spark-3.0.1-bin-hadoop3.2.tgz && \
    mv spark-3.0.1-bin-hadoop3.2/ /usr/local/spark && \
    wget https://archive.apache.org/dist/kafka/1.1.0/kafka_2.11-1.1.0.tgz && \
    tar -xzf kafka_2.11-1.1.0.tgz && \
    mv kafka_2.11-1.1.0 /usr/local/kafka && \
    ln -s /usr/local/spark spark

WORKDIR app
COPY . /app
RUN pip3 install cython==0.29.21 numpy==1.18.5 && pip3 install tweepy pytest pyspark pandas==1.0.5 requests requests-oauthlib kafka-python
ENV PYSPARK_PYTHON=python3
