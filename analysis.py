import pandas as pd

# Load the dataset
data = pd.read_csv("./data/archive/fraudTrain.csv")

# Select relevant columns for anomaly detection
transactions = data[['trans_date_trans_time', 'cc_num', 'category', 'amt', 'lat', 'long', 'merch_lat', 'merch_long', 'city_pop', 'unix_time', 'is_fraud']]

# Convert 'trans_date_trans_time' to datetime for time-based analysis
transactions['trans_date_trans_time'] = pd.to_datetime(transactions['trans_date_trans_time'])

# Normalize latitude and longitude values
transactions['lat'] = transactions['lat'] / 90  # Latitude ranges from -90 to 90
transactions['long'] = transactions['long'] / 180  # Longitude ranges from -180 to 180
transactions['merch_lat'] = transactions['merch_lat'] / 90
transactions['merch_long'] = transactions['merch_long'] / 180

# Preview the dataset structure
print(transactions.head())
