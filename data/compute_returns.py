import os
import pandas as pd
import numpy as np

try:
    print("Returns script started")
    print("Working directory:", os.getcwd())

    price_path = 'data/price_data.csv'
    if not os.path.exists(price_path):
        raise FileNotFoundError(f"{price_path} not found")

    prices = pd.read_csv(price_path, index_col=0, parse_dates=True)
    print("Loaded price_data.csv with shape", prices.shape)

    simple_ret = prices.pct_change().dropna()
    simple_ret.to_csv('data/simple_returns.csv')
    print("✅ simple_returns.csv saved")

    log_ret = np.log(prices / prices.shift(1)).dropna()
    log_ret.to_csv('data/log_returns.csv')
    print("✅ log_returns.csv saved")

except Exception as e:
    print("❌ ERROR:", e)
