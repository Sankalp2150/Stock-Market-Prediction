import pandas as pd
from alpha_vantage.timeseries import TimeSeries

def fetch_historical_data_from_alpha(symbol, api_key):
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='full')
        data = data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        data = data[::-1]  # reverse so oldest first
        data.dropna(inplace=True)
        return data
    except Exception as e:
        print(f"Alpha Vantage API error for {symbol}: {e}")
        return pd.DataFrame()