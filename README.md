# **RiskSense: Real-Time Anomaly Detection in Financial Data Streams**

**RiskSense** is a real-time financial anomaly detection system built using **Apache Kafka**, **Apache Spark**, **TensorFlow**, **Flask**, **Redis**, and **Docker**. It uses an autoencoder-based deep learning model to detect anomalies (e.g., fraudulent transactions) in streaming financial data. The system is optimized for real-time detection and performance, with caching and high scalability.

## **Features**

- **Real-time anomaly detection** for financial data streams.
- Autoencoder-based model trained on financial transaction data.
- Deployed API to monitor and detect fraudulent transactions in real-time.
- Caching with Redis for faster processing of repeated transactions.
- Dockerized for easy setup and deployment.

## **Technologies Used**

- **Apache Kafka**: Streaming financial transaction data.
- **Apache Spark**: Real-time data processing and anomaly detection.
- **TensorFlow**: Deep learning model (autoencoder) for detecting anomalies.
- **Flask**: API to monitor and query anomalies in real-time.
- **Redis**: Caching system to speed up anomaly detection in repeated queries.
- **Docker**: Containerization for easy setup and deployment.

## **Project Structure**

```plaintext
risk-sense/
│
├── docker-compose.yml         # Docker Compose file
├── Dockerfile                 # Dockerfile for Flask, Spark, and TensorFlow
│
├── model/                     # Model training and loading scripts
│   └── train_model.py         # Script to train the autoencoder for anomaly detection
│   └── load_model.py          # Script to load the trained model for real-time inference
│
├── app/                       # Flask app for real-time anomaly detection API
│   └── app.py                 # Flask application to handle requests
│
├── data/                      # Financial transaction data
│   └── fraudTrain.csv         # Sample financial transactions with fraud flags
│
├── kafka/                     # Kafka producer for streaming transactions
│   └── kafka_producer.py      # Producer script to stream transaction data to Kafka
│
├── spark/                     # Spark consumer for processing and detecting anomalies
│   └── spark_consumer.py      # Spark application to consume transactions from Kafka
│
├── cache/                     # Redis cache handling
│   └── redis_cache.py         # Redis cache logic for optimizing latency
│
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation and setup instructions
