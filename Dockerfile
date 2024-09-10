# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for h5py, Java, and PySpark
RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev \
    gcc \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
RUN export JAVA_HOME

# Increase pip timeout
ENV PIP_DEFAULT_TIMEOUT=1000

# Copy the requirements.txt file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Default command
CMD ["python", "kafka/kafka_producer.py"]
