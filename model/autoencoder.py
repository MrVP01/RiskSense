import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
import numpy as np

# Load the dataset
data = pd.read_csv("data/fraudTrain.csv")

# Filter non-fraudulent transactions for training
normal_transactions = data[data['is_fraud'] == 0][['amt', 'lat', 'long', 'merch_lat', 'merch_long', 'city_pop']].values

# Normalize the amount and city population
normal_transactions[:, 0] = normal_transactions[:, 0] / max(normal_transactions[:, 0])  # Amount
normal_transactions[:, 5] = normal_transactions[:, 5] / max(normal_transactions[:, 5])  # City population

# Build the autoencoder
def create_autoencoder(input_dim):
    model = Sequential([
        Dense(32, activation='relu', input_shape=(input_dim,)),
        Dense(16, activation='relu'),
        Dense(8, activation='relu'),
        Dense(16, activation='relu'),
        Dense(32, activation='relu'),
        Dense(input_dim, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

autoencoder = create_autoencoder(normal_transactions.shape[1])

# Train the model
autoencoder.fit(normal_transactions, normal_transactions, epochs=50, batch_size=32)

# Save the trained model
autoencoder.save('models/trained_model.h5')
