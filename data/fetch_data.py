import os
import pandas as pd
import yfinance as yf

try:
    print("Script started")
    print("Working directory:", os.getcwd())

    if not os.path.exists('data/tickers.csv'):
        raise FileNotFoundError("data/tickers.csv not found")


    tickers = (
        pd.read_csv('data/tickers.csv', header=None)[0]
          .str.strip()
          .tolist()
    )
    print("Loaded tickers:", tickers)

 
    data = yf.download(
        tickers,
        start="2020-01-01",
        end="2024-01-01",
        interval="1d",
        auto_adjust=True
    )['Close']
    print("Downloaded data for:", data.columns.tolist())

   
    data.to_csv('data/price_data.csv')
    print("✅ Data successfully fetched and saved to data/price_data.csv")

except Exception as e:
    print("❌ ERROR:", e)
