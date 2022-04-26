from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys

def aggregate_tags_count(new_values, total_sum):
	return sum(new_values) + (total_sum or 0)

def get_sql_context_instance(spark_context):
  if ('sqlContextSingletonInstance' not in globals()):
    globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
  return globals()['sqlContextSingletonInstance']

def process_rdd(time, rdd):
  print("----------- %s -----------" % str(time))
  try:
    sql_context = get_sql_context_instance(rdd.context)
    row_rdd = rdd.map(lambda w: Row(hashtag=w[0], hashtag_count=w[1]))
    hashtags_df = sql_context.createDataFrame(row_rdd)
    hashtags_df.registerTempTable("hashtags")
    hashtag_counts_df = sql_context.sql("select hashtag, hashtag_count from hashtags order by hashtag_count desc limit 10")
    hashtag_counts_df.show()
  except:
    e = sys.exc_info()[0]
    print("Error: %s" % e)

IP_ADDRESS = "localhost"
PORT = 9009
INTERVAL_IN_SECONDS = 2

conf = SparkConf()
conf.setAppName("TwitterStreamSparkIngestion")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, INTERVAL_IN_SECONDS)
ssc.checkpoint("checkpoint_TwitterApp")
dataStream = ssc.socketTextStream(IP_ADDRESS, PORT)

words = dataStream.flatMap(lambda line: line.split(" "))
hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))
tags_totals = hashtags.updateStateByKey(aggregate_tags_count)
tags_totals.foreachRDD(process_rdd)
ssc.start()
ssc.awaitTermination()
