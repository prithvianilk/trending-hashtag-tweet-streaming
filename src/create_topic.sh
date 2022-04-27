KAFKA_PATH="/usr/local/kafka"

${KAFKA_PATH}/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic machi