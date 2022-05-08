# Twitter Data Streaming


## Project Details

### The project consists of

1. Streaming tweets with trending hashtags to Spark. 
2. Publishing tweet datato Kafka where each hashtag is the topic name and the number of tweets within a time window is the message. 
3. Consuming from Kafka and inserting each message as a document in MongoDB.

## Steps to start project

1. Build the docker image.
`docker build -t dbt-project .`

2. Run the docker container
`./scripts/start.sh`

3. [Update `/opt/kafka/bin/kafka-run-class.sh`](https://stackoverflow.com/questions/50513744/apache-kafka-2-12-1-1-0-not-working-with-jdk-10-0-1)

4. Start Zookeper server `./scripts/start_zookeeper.sh`
5. Start Kafka server `./scripts/start_kafka.sh`
6. Start Mongo Server `./scritps/start_mongod.sh`
7. Start tweet collection script `python3 src/twitter_hashtag_streaming.py`
8. Start spark ingestion server `python3 src/hashtag_count_spark_streaming.py`
9. Start Kafka consumption script `python3 src/hashtag_kafka_consumer.py`