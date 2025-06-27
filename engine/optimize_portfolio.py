import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns

def main():
   
    prices = pd.read_csv('data/price_data.csv', index_col=0, parse_dates=True)

    mu = expected_returns.mean_historical_return(prices)
    S  = risk_models.sample_cov(prices)

    ef = EfficientFrontier(mu, S)
    ef.max_sharpe()
    weights = ef.clean_weights()

    ef.portfolio_performance(verbose=True)
    print("\nOptimized Weights:")
    for ticker, w in weights.items():
        if w > 1e-4:
            print(f"  {ticker}: {w:.2%}")

   
    pd.Series(weights).to_csv('data/optimized_weights.csv')
    print("\n✅ Saved optimized_weights.csv")

if __name__ == "__main__":
    main()
