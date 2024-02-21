# importing System dependencies #running
import os
import sys
import json #added
#from pyspark.sql.types import * #added



# Setting up enviroment
os.environ["PYSPARK_PYTHON"] = "/opt/cloudera/parcels/Anaconda/bin/python"
os.environ["JAVA_HOME"] = "/usr/java/jdk1.8.0_161/jre"
os.environ["SPARK_HOME"] = "/opt/cloudera/parcels/SPARK2-2.3.0.cloudera2-1.cdh5.13.3.p0.316101/lib/spark2/"
os.environ["PYLIB"] = os.environ["SPARK_HOME"] + "/python/lib"
sys.path.insert(0, os.environ["PYLIB"] +"/py4j-0.10.6-src.zip")
sys.path.insert(0, os.environ["PYLIB"] +"/pyspark.zip")

# importing required pyspark modules
from pyspark.sql import SparkSession #col added
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.types import MapType,StringType # added
from pyspark.sql.functions import from_json,col#added


# Initialize spark session
spark = SparkSession\
    .builder \
    .appName("UserFeedbackWriter") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Server and topic Details
serverDetails = "18.211.252.152:9092"
topicName = "user-feedback"

# Defining Schema 
schema = StructType() \
    .add("request_id",StringType()) \
    .add("campaign_id",StringType()) \
    .add("user_id",StringType()) \
    .add("click",IntegerType()) \
    .add("view",IntegerType()) \
    .add("acquisition",IntegerType()) \
    .add("auction_cpm",DoubleType()) \
    .add("auction_cpc",DoubleType()) \
    .add("auction_cpa",DoubleType()) \
    .add("target_age_range",StringType()) \
    .add("target_Location",StringType()) \
    .add("target_gender",StringType()) \
    .add("target_income_bucket",StringType()) \
    .add("target_device_type",StringType()) \
    .add("campaign_start_time",StringType()) \
    .add("campaign_end_time",StringType()) \
    .add("user_action",StringType()) \
    .add("expenditure",DoubleType()) \
    .add("timestamp",StringType())

#Read Input from Kafka
dataRead = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers",serverDetails) \
    .option("startingOffsets","Latest") \
    .option("subscribe",topicName) \
    .load()

#Reading json data based on created schema
#print('done reading from kafka') # added
dataStream = dataRead.select(from_json(col("value").cast("string"),schema).alias("data")).select("data.*")
#print('done reading JSON') # added extar

# Writing feedback data to HDFS as CSV for archiving and billing purposes
HDFSSink = dataStream \
    .writeStream \
    .format('csv') \
    .outputMode("append") \
    .option("truncate","false") \
    .option("path","op11") \
    .option("checkpointLocation","cp11") \
    .trigger(processingTime="1 minute") \
    .start()
# Waitig for process to complete
HDFSSink.awaitTermination()
#end
