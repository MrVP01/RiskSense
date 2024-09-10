from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, DoubleType, LongType, StringType
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

# Define schema for incoming transaction data
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

# Load the trained autoencoder model
import tensorflow as tf
autoencoder = tf.keras.models.load_model('/app/models/trained_model.h5')

# Store predictions and actual values for evaluation
predictions = []
actuals = []

def detect_anomaly(transaction, model, threshold=0.1):
    # Prepare the feature vector
    transaction_vector = np.array([[
        transaction["amount"],
        transaction["latitude"],
        transaction["longitude"],
        transaction["merchant_lat"],
        transaction["merchant_long"],
        transaction["city_pop"]
    ]])
    
    # Normalize the feature vector (using the max values from the training data)
    transaction_vector[:, 0] = transaction_vector[:, 0] / max_amount  # Amount
    transaction_vector[:, 5] = transaction_vector[:, 5] / max_city_pop  # City population

    # Predict and compute reconstruction error
    reconstruction = model.predict(transaction_vector)
    loss = np.mean(np.abs(reconstruction - transaction_vector))
    
    return loss > threshold  # Return True if anomaly detected

def process_row(row):
    transaction = row.asDict()

    # Detect anomaly
    is_anomaly = detect_anomaly(transaction, autoencoder)
    
    # Append prediction (1 if anomaly detected, else 0) and actual label (is_fraud)
    predictions.append(1 if is_anomaly else 0)
    actuals.append(transaction['is_fraud'])

    # Print result for each transaction
    if is_anomaly:
        print(f"Anomaly detected: Transaction ID {transaction['transaction_id']}, Amount: {transaction['amount']}")
    else:
        print(f"Normal Transaction: ID {transaction['transaction_id']}, Amount: {transaction['amount']}")

# Apply the function to the streaming data
df.writeStream.foreach(process_row).start().awaitTermination()

# After processing, compute confusion matrix and classification report
def evaluate_model():
    print("\nEvaluation Metrics:")
    print(confusion_matrix(actuals, predictions))
    print(classification_report(actuals, predictions))

# Call evaluate_model() at the end of the stream (or after a batch of transactions)
evaluate_model()
