# utils.py
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

ALPHA_VANTAGE_API_KEY = 'YOUR_API_KEY'  # Replace this with your real Alpha Vantage API key

def fetch_from_alpha_vantage(symbol, api_key):
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
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

def fetch_historical_data_from_alpha(symbol, api_key):
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta = ts.get_daily(symbol=symbol, outputsize='full')
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
        print(f"Alpha Vantage historical fetch failed for {symbol}: {e}")
        return pd.DataFrame()