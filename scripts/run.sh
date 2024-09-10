#!/bin/bash

# Start Kafka producer to simulate transaction streaming
python kafka/kafka_producer.py &

# Run Spark streaming consumer for real-time anomaly detection
python spark/spark_consumer.py
