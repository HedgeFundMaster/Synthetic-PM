#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path

import pandas as pd
import numpy as np

from engine.murphy_risk_model import simulate_murphy_risk, murphy_summary_stats, plot_murphy_simulations


def setup_logger() -> None:
    """Configure root logger for consistent formatting."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_data(
    returns_path: Path,
    weights_path: Path,
    drawdown_path: Path
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Load and align returns, weights, and drawdown data.
    """
    rets = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    w_df = pd.read_csv(weights_path, index_col=0)
    w = w_df.iloc[:, 0]
    dd = pd.read_csv(drawdown_path, index_col=0, parse_dates=True).iloc[:, 0]
    common = rets.columns.intersection(w.index)
    rets_aligned = rets[common]
    w_aligned = w.loc[common]
    return rets_aligned, w_aligned, dd


def compute_metrics(
    rets: pd.DataFrame, weights: pd.Series, drawdown: pd.Series
) -> dict[str, float]:
    """
    Compute portfolio-level performance metrics.
    """
    port_ret = rets.dot(weights)
    # Annualized stats
    ann_ret = (1 + port_ret).prod() ** (252 / len(port_ret)) - 1
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = ann_ret / ann_vol if ann_vol else np.nan

    # Benchmark for beta/alpha
    bench = rets['SPY'] if 'SPY' in rets.columns else rets.mean(axis=1)
    df = pd.concat([port_ret.rename('Portfolio'), bench.rename('Benchmark')], axis=1).dropna()
    beta, alpha_daily = np.polyfit(df['Benchmark'], df['Portfolio'], 1)
    alpha_ann = alpha_daily * 252
    max_dd = drawdown.min()

    return {
        'Annualized Return': ann_ret,
        'Annualized Volatility': ann_vol,
        'Sharpe Ratio': sharpe,
        'Beta': beta,
        'Daily Alpha': alpha_daily,
        'Annual Alpha': alpha_ann,
        'Max Drawdown': max_dd,
    }


def save_metrics(metrics: dict[str, float], output_path: Path) -> None:
    """Save metrics to CSV in a tidy two-column format."""
    df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
    df.to_csv(output_path)
    logging.info(f"Metrics saved to {output_path}")


def run_murphy(
    port_ret: pd.Series,
    output_path: Path,
    simulations: int
) -> None:
    """
    Execute Monte Carlo Murphy risk simulations and save summary.
    """
    logging.info("Starting Murphy risk Monte Carlo simulation...")
    sims = simulate_murphy_risk(port_ret, n_simulations=simulations)
    plot_murphy_simulations(sims)
    stats = murphy_summary_stats(sims)
    stats_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Value'])
    stats_df.to_csv(output_path)
    for k, v in stats.items():
        logging.info(f"Murphy {k}: {v:.4f}")
    logging.info(f"Murphy metrics saved to {output_path}")


def main() -> None:
    setup_logger()
    parser = argparse.ArgumentParser(description="Portfolio metrics with optional Murphy risk")
    parser.add_argument('--returns', type=Path, default='data/simple_returns.csv')
    parser.add_argument('--weights', type=Path, default='data/optimized_weights.csv')
    parser.add_argument('--drawdown', type=Path, default='data/portfolio_drawdown.csv')
    parser.add_argument('--output', type=Path, default='data/metrics_summary.csv')
    parser.add_argument('--murphy', action='store_true', help='Run Murphy risk simulations')
    parser.add_argument('--murphy-sims', type=int, default=5000, help='Number of Murphy simulation paths')
    args = parser.parse_args()

    logging.info("Loading data...")
    rets, w, dd = load_data(args.returns, args.weights, args.drawdown)

    logging.info("Computing performance metrics...")
    metrics = compute_metrics(rets, w, dd)
    for name, val in metrics.items():
        logging.info(f"{name}: {val:.4f}")
    save_metrics(metrics, args.output)

    if args.murphy:
        # Use portfolio return series for Murphy
        port_ret = rets.dot(w)
        run_murphy(port_ret, output_path=Path('data/murphy_metrics.csv'), simulations=args.murphy_sims)

if __name__ == '__main__':
    main()
