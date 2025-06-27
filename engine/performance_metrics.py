import pandas as pd
import yfinance as yf
import os

def main():

    rets = pd.read_csv('data/simple_returns.csv', index_col=0, parse_dates=True)
    print("Loaded simple_returns.csv with shape", rets.shape)


    bench_prices = yf.download(
        "SPY",
        start="2020-01-01",
        end="2024-01-01",
        interval="1d",
        auto_adjust=True
    )["Close"]
    bench = bench_prices.pct_change().dropna()
    bench.name = "SPY"  
    print("Fetched SPY returns with length", len(bench))


    df = rets.join(bench, how="inner")
    print("Merged data shape:", df.shape)


    results = {}
    var_bench  = df["SPY"].var()
    mean_bench = df["SPY"].mean()

    for col in rets.columns:
        cov   = df[col].cov(df["SPY"])
        beta  = cov / var_bench
        alpha = df[col].mean() - beta * mean_bench
        results[col] = {"beta": beta, "alpha": alpha}

    metrics = pd.DataFrame(results).T
    metrics.index.name = "Ticker"


    metrics.to_csv("data/asset_alpha_beta.csv")
    print("\nAsset β & α:\n", metrics)

if __name__ == "__main__":
    main()