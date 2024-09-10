from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, DoubleType, LongType, StringType

# Define schema for the incoming transaction data
schema = StructType([
    StructField("transaction_id", LongType(), True),
    StructField("credit_card", LongType(), True),
    StructField("amount", DoubleType(), True),
    StructField("merchant_category", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("merchant_lat", DoubleType(), True),
    StructField("merchant_long", DoubleType(), True),
    StructField("city_pop", LongType(), True),
    StructField("unix_time", LongType(), True),
    StructField("is_fraud", LongType(), True)
])

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RealTimeFraudDetection") \
    .getOrCreate()

# Read the Kafka stream
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "financial-transactions") \
    .load()

# Parse the JSON messages
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Display transactions in real-time (for testing)
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
