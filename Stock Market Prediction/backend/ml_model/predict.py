import os
import pandas as pd
import yfinance as yf
import joblib
from alpha_vantage.timeseries import TimeSeries
import json

model_dir = "/Users/sankalprana/Desktop/Stock-Market-Prediction/Stock Market Prediction/backend/ml_model/models"
ALPHA_VANTAGE_API_KEY = "RB7YKRU3XH8QI7JC"  # Ideally load from env for security

def fetch_from_alpha_vantage(symbol):
    try:
        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        data, meta = ts.get_daily(symbol=symbol, outputsize='compact')
        data = data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        data = data[::-1]  # Sort from oldest to newest
        data.dropna(inplace=True)
        return data
    except Exception as e:
        print(f"Alpha Vantage failed for {symbol}: {e}")
        return pd.DataFrame()

def get_latest_features(symbol):
    df = yf.download(symbol, period="1mo", interval="1d")
    df.dropna(inplace=True)

    if df.shape[0] < 20:
        print(f"No data from yfinance for {symbol}, trying Alpha Vantage...")
        df = fetch_from_alpha_vantage(symbol)
        if df.empty or df.shape[0] < 20:
            print(f"Not enough data to generate features for {symbol}")
            return pd.DataFrame()

    # Feature engineering consistent with training
    df['High-Low'] = df['High'] - df['Low']
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()

    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df.dropna(inplace=True)

    latest = df.iloc[-1]
    features = {
        'Close': latest['Close'],
        'High-Low': latest['High-Low'],
        'SMA_5': latest['SMA_5'],
        'EMA_20': latest['EMA_20'],
        'RSI': latest['RSI']
    }

    return pd.DataFrame([features])

def load_model_and_predict(symbol):
    import math

    model_path = os.path.join(model_dir, f"{symbol}_model.pkl")
    scaler_path = os.path.join(model_dir, f"{symbol}_scaler.pkl")

    print(f"Looking for model at: {model_path}")
    print(f"Looking for scaler at: {scaler_path}")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Model or scaler not found for {symbol}")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    features = get_latest_features(symbol)
    if features.empty:
        raise ValueError(f"Could not generate prediction — insufficient data for {symbol}")

    print("Features to predict on:", features)
    print("Feature columns:", features.columns.tolist())

    try:
        X_scaled = scaler.transform(features)
        prediction = model.predict(X_scaled)
    except Exception as e:
        print(f"Prediction error: {e}")
        raise e

    # Load saved training accuracy
    meta_path = os.path.join(model_dir, f"{symbol}_meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            metadata = json.load(f)
            accuracy = metadata.get("accuracy", 0.0)
    else:
        accuracy = 0.0

    return {
        "predicted_price": float(prediction[0]),
        "accuracy": round(accuracy, 2)
    }

def get_historical_comparison_data(symbol):
    df = yf.download(symbol, period="1mo", interval="1d")
    df.dropna(inplace=True)

    if df.empty or 'Close' not in df.columns:
        raise ValueError(f"No valid historical data found for {symbol}")

    dates = pd.Series(df.index).dt.strftime('%Y-%m-%d').tolist()
    close_prices = df['Close'].values.tolist()

    return {
        "dates": dates,
        "close_prices": close_prices
    }

if __name__ == "__main__":
    symbol = 'AAPL'
    try:
        result = load_model_and_predict(symbol)
        print(f"Predicted next close price for {symbol}: ${result['predicted_price']:.2f} with accuracy {result['accuracy']:.2f}%")
    except Exception as e:
        print(f"Prediction error: {e}")