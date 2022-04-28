KAFKA_PATH="/opt/kafka"

${KAFKA_PATH}/bin/kafka-topics.sh --list --zookeeper localhost:2181
echo 
${KAFKA_PATH}/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic machi
