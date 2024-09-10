from kafka import KafkaProducer
import json
import time
import pandas as pd

# Load the dataset
data = pd.read_csv("./data/fraudTrain.csv")

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Stream transactions to Kafka
for index, row in data.iterrows():
    transaction = {
        "transaction_id": index,
        "credit_card": row["cc_num"],
        "amount": row["amt"],
        "merchant_category": row["category"],
        "latitude": row["lat"],
        "longitude": row["long"],
        "merchant_lat": row["merch_lat"],
        "merchant_long": row["merch_long"],
        "city_pop": row["city_pop"],
        "unix_time": row["unix_time"],
        "is_fraud": row["is_fraud"]
    }
    
    # Send transaction data to Kafka topic 'financial-transactions'
    producer.send('financial-transactions', value=transaction)
    
    # Simulate real-time streaming by sending a transaction every second
    time.sleep(1)
