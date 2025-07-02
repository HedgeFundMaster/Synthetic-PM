# engine/optimize_portfolio.py

import logging
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.objective_functions import L2_reg

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def main():
    setup_logger()
    logging.info("Loading price data from data/price_data.csv")
    prices = pd.read_csv('data/price_data.csv', index_col=0, parse_dates=True)

    logging.info("Estimating expected returns and covariance matrix")
    mu = expected_returns.mean_historical_return(prices)
    S = risk_models.sample_cov(prices)

    logging.info("Initializing Efficient Frontier optimizer")
    ef = EfficientFrontier(mu, S)

    # Apply constraints BEFORE calling max_sharpe()
    logging.info("Adding no‐short constraint (w >= 0)")
    ef.add_constraint(lambda w: w >= 0)
    logging.info("Adding max‐weight constraint (w <= 0.20)")
    ef.add_constraint(lambda w: w <= 0.20)

    # Optional regularization to smooth weights
    logging.info("Adding L2 regularization (gamma=0.01)")
    ef.add_objective(L2_reg, gamma=0.01)

    logging.info("Optimizing for maximum Sharpe ratio under constraints")
    raw_weights = ef.max_sharpe()
    weights = ef.clean_weights()

    logging.info("Post‐optimization portfolio performance:")
    ef.portfolio_performance(verbose=True)

    logging.info("Final weight vector (only nonzero weights shown):")
    for ticker, w in weights.items():
        if w > 1e-4:
            logging.info(f"  {ticker}: {w:.2%}")

    # Save weights
    out_path = 'data/optimized_weights.csv'
    pd.Series(weights).to_csv(out_path)
    logging.info(f"Saved optimized weights to {out_path}")

if __name__ == "__main__":
    main()

