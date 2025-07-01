import os
import pandas as pd

def main():
    print("Drawdown analysis started")

    # 1) Load simple returns
    rets = pd.read_csv(
        'data/simple_returns.csv', index_col=0, parse_dates=True
    )
    print("Loaded simple_returns.csv with shape", rets.shape)

    # 2) Load optimized weights
    # Read with header=0 to correctly parse ticker symbols
    w_df = pd.read_csv(
        'data/optimized_weights.csv', index_col=0
    )
    # The first column is the weights
    w = w_df.iloc[:, 0].dropna()
    print(f"Loaded optimized_weights.csv with {len(w)} tickers")

    # 3) Align tickers between returns and weights
    common = rets.columns.intersection(w.index)
    if len(common) < len(w):
        missing = w.index.difference(rets.columns)
        print(f"⚠️ Warning: The following tickers have weights but no return data: {list(missing)}")
    if len(common) < len(rets.columns):
        extra = rets.columns.difference(w.index)
        print(f"ℹ️ Note: The following tickers have return data but no weights (will be ignored): {list(extra)}")
    rets_aligned = rets[common]
    w_aligned = w[common]

    # 4) Compute portfolio return series
    port_ret = rets_aligned.dot(w_aligned)
    port_cum = (1 + port_ret).cumprod()
    print("Computed cumulative returns—last value:", port_cum.iloc[-1])

    # 5) Compute drawdown series
    roll_max = port_cum.cummax()
    drawdown = (port_cum - roll_max) / roll_max
    max_dd = drawdown.min()
    print(f"Max drawdown: {max_dd:.2%}")

    # 6) Save drawdown series
    out_path = 'data/portfolio_drawdown.csv'
    drawdown.to_csv(out_path, header=['Drawdown'])
    print(f"✅ Saved drawdown series to {out_path}")

if __name__ == "__main__":
    main()

