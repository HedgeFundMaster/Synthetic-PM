# engine/murphy_report.py
#!/usr/bin/env python3
import logging
from pathlib import Path

import pandas as pd

from engine.murphy_report import (
    simulate_murphy_risk,
    murphy_summary_stats,
    plot_murphy_simulations,
)

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    setup_logger()
    logging.info("Loading portfolio returns from data/simple_returns.csv")
    rets = pd.read_csv(
        "data/simple_returns.csv", index_col=0, parse_dates=True
    )
    # Use true portfolio returns if available; fallback to average
    port_ret = rets.mean(axis=1)

    logging.info("Running Monte Carlo Murphy simulation...)
    sims = simulate_murphy_risk(
        portfolio_returns=port_ret,
        n_simulations=5000,
        n_days=252,
        shock_probability=0.02,
        shock_magnitude=-0.20,
    )

    logging.info("Plotting simulation paths...")
    plot_murphy_simulations(sims, n_show=200)

    logging.info("Computing summary statistics...")
    stats = murphy_summary_stats(sims)
    for k, v in stats.items():
        logging.info(f"{k}: {v:.4f}")

    out_path = Path("data/murphy_metrics.csv")
    pd.DataFrame.from_dict(stats, orient="index", columns=["Value"]).to_csv(out_path)
    logging.info(f"Saved Murphy stats to {out_path}")

if __name__ == "__main__":
    main()
