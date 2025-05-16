import sys
import os

# Force Python to include the backend folder in the import path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
import joblib
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from utils.data_fetch import fetch_historical_data_from_alpha

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

def create_features(df):
    df['High-Low'] = df['High'] - df['Low']
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df.dropna(inplace=True)
    return df

def fetch_data(symbol):
    df = yf.download(symbol, period="10y", interval="1d")
    if df.empty or df.shape[0] < 1000:
        print(f"No or insufficient data from yfinance for {symbol}, trying Alpha Vantage...")
        df = fetch_historical_data_from_alpha(symbol)
    if df.empty or df.shape[0] < 1000:
        raise ValueError(f"Not enough data to train for {symbol}")
    return df

def train_and_save_model(symbol):
    print(f"Starting training for {symbol}...")
    df = fetch_data(symbol)
    df = create_features(df)

    features = df[['Close', 'High-Low', 'SMA_5', 'EMA_20', 'RSI']]
    target = df['Close'].shift(-1).dropna()
    features = features[:-1]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, target, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test) * 100
    print(f"✅ Finished training {symbol}. Test R² accuracy: {accuracy:.4f}")

    # Save model and scaler
    joblib.dump(model, os.path.join(MODEL_DIR, f"{symbol}_model.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, f"{symbol}_scaler.pkl"))

    # Save metadata with accuracy
    metadata = {"symbol": symbol, "accuracy": round(accuracy, 2)}
    with open(os.path.join(MODEL_DIR, f"{symbol}_meta.json"), "w") as f:
        json.dump(metadata, f)

def main():
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    # Delete old models
    for file in os.listdir(MODEL_DIR):
        if file.endswith(".pkl"):
            os.remove(os.path.join(MODEL_DIR, file))

    for symbol in symbols:
        try:
            train_and_save_model(symbol)
        except Exception as e:
            print(f"[ERROR] Training failed for {symbol}: {e}")

if __name__ == "__main__":
    main()