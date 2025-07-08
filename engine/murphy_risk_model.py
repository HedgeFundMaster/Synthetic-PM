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
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def load_data(returns_path: Path, weights_path: Path, drawdown_path: Path):
    """
    Load returns, weights, and drawdown series; align tickers.
    Returns:
        rets_aligned (pd.DataFrame), w_aligned (pd.Series), drawdown (pd.Series)
    """
    rets = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    w_df = pd.read_csv(weights_path, index_col=0)
    w = w_df.iloc[:, 0]
    dd = pd.read_csv(drawdown_path, index_col=0, parse_dates=True).iloc[:, 0]
    # Align tickers
    common = rets.columns.intersection(w.index)
    rets_aligned = rets[common]
    w_aligned = w.loc[common]
    return rets_aligned, w_aligned, dd


def compute_metrics(rets: pd.DataFrame, weights: pd.Series, drawdown: pd.Series) -> dict:
    """
    Compute performance metrics: ann return, vol, Sharpe, beta, alpha, max drawdown.
    """
    port_ret = rets.dot(weights)
    ann_ret = (1 + port_ret).prod() ** (252 / len(port_ret)) - 1
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = ann_ret / ann_vol
    # Benchmark
    if 'SPY' in rets.columns:
        bench_ret = rets['SPY']
    else:
        bench_ret = rets.mean(axis=1)
    df = pd.concat([port_ret.rename('Portfolio'), bench_ret.rename('Benchmark')], axis=1).dropna()
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
        'Max Drawdown': max_dd
    }


def save_metrics(metrics: dict, output_path: Path) -> None:
    """Save metrics dict to CSV."""
    df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
    df.to_csv(output_path)
    logging.info(f"Metrics saved to {output_path}")


def run_murphy(port_ret: pd.Series, output_dir: Path) -> None:
    """Run Monte Carlo Murphy simulation and save summary."""
    sims = simulate_murphy_risk(port_ret)
    plot_murphy_simulations(sims)
    stats = murphy_summary_stats(sims)
    for k, v in stats.items():
        logging.info(f"Murphy {k}: {v:.4f}")
    # Save stats
    murphy_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Value'])
    murphy_path = output_dir / 'murphy_metrics.csv'
    murphy_df.to_csv(murphy_path)
    logging.info(f"Murphy metrics saved to {murphy_path}")


def main():
    parser = argparse.ArgumentParser(description="Portfolio metrics report with optional Murphy stress tests")
    parser.add_argument('--returns', default='data/simple_returns.csv', help='Path to returns CSV')
    parser.add_argument('--weights', default='data/optimized_weights.csv', help='Path to weights CSV')
    parser.add_argument('--drawdown', default='data/portfolio_drawdown.csv', help='Path to drawdown CSV')
    parser.add_argument('--output', default='data/metrics_summary.csv', help='Output CSV for metrics')
    parser.add_argument('--murphy', action='store_true', help='Run Monte Carlo Murphy risk simulation')
    args = parser.parse_args()

    setup_logger()
    logging.info("Starting metrics report")

    returns_path = Path(args.returns)
    weights_path = Path(args.weights)
    drawdown_path = Path(args.drawdown)
    output_path = Path(args.output)

    rets, w, dd = load_data(returns_path, weights_path, drawdown_path)
    metrics = compute_metrics(rets, w, dd)
    save_metrics(metrics, output_path)

    # If Murphy flag, run Monte Carlo stress tests
    port_ret = rets.dot(w)
    if args.murphy:
        run_murphy(port_ret, output_path.parent)

if __name__ == '__main__':
    main()

