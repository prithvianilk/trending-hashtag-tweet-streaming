from kafka import KafkaProducer
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from constants import APP_NAME, HASHTAGS, PORT, HOST, TIME_WINDOW_IN_SECONDS


def publish_topics_to_kafka(values):
    for hashtag, count in values:
        producer.send(hashtag[1 :], str(count).encode('utf-8'))
        producer.flush()

producer = KafkaProducer(bootstrap_servers='localhost:9092')
sc = SparkContext(appName=APP_NAME)
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, TIME_WINDOW_IN_SECONDS)
lines = ssc.socketTextStream(HOST, PORT)
counts = lines.flatMap(lambda line: line.split(" ")) \
              .filter(lambda w: '#' in w) \
              .filter(lambda w: w in HASHTAGS) \
              .map(lambda word: (word, 1)) \
              .reduceByKey(lambda a, b: a + b) \
              .foreachRDD(lambda x: publish_topics_to_kafka(x.collect()))

ssc.start()
ssc.awaitTermination()
