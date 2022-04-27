from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    hashtags =['#ElonMusk',"#Ukraine","#IPL","#Valorant","#KGFChapter2"]
    sc = SparkContext(appName="PythonStreamingNetworkWordCount")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 3)
    lines = ssc.socketTextStream("localhost", 9008)
    counts = lines.flatMap(lambda line: line.split(" "))\
                  .filter(lambda w: '#' in w)\
                  .filter(lambda w: w in hashtags)\
                  .map(lambda word: (word, 1))\
                  .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
