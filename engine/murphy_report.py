#!/usr/bin/env python3
# engine/murphy_report.py

import logging

import pandas as pd

# Import Murphy model functions from same directory
from murphy_risk_model import (
    simulate_murphy_risk,
    murphy_summary_stats,
    plot_murphy_simulations,
)

def setup_logger():
    """Configure root logger for consistent formatting."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    setup_logger()
    logging.info("Loading portfolio returns from data/simple_returns.csv")
    rets = pd.read_csv("data/simple_returns.csv", index_col=0, parse_dates=True)
    port_ret = rets.mean(axis=1)  # replace with weighted returns if available

    logging.info("Running Murphy Monte Carlo simulation")

    sims = simulate_murphy_risk(
        portfolio_returns=port_ret,
        n_simulations=5000,
        n_days=252,
        shock_probability=0.02,
        shock_magnitude=-0.20,
    )

    logging.info("Plotting simulation paths")
    plot_murphy_simulations(sims, n_show=200)

    logging.info("Computing summary statistics")
    stats = murphy_summary_stats(sims)
    print("\nMurphy Risk Summary:")
    for k, v in stats.items():
        print(f"{k}: {v:.4f}")

    # Save to CSV
    pd.Series(stats).to_csv("data/murphy_summary.csv")
    logging.info("✅ Saved murphy_summary.csv")

if __name__ == "__main__":
    main()