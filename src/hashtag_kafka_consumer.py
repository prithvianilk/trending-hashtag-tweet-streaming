from kafka import KafkaConsumer
from pymongo import MongoClient
from constants import HASHTAGS


TOPICS = list(map(lambda x: x[1: ], HASHTAGS))

client = MongoClient('localhost', 27017)
db = client.dbt
hashtags_collection = db.hashtags

consumer = KafkaConsumer(*TOPICS)
for message in consumer:
    topic = message.topic
    count = int(message.value)
    print(topic, count)
    hashtags_collection.insert_one({ 'hashtag': topic, 'count': count })