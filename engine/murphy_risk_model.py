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


def load_data(returns_path: Path, weights_path: Path, drawdown_path: Path):
    rets = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    w_df = pd.read_csv(weights_path, index_col=0)
    w = w_df.iloc[:, 0]
    dd = pd.read_csv(drawdown_path, index_col=0, parse_dates=True).iloc[:, 0]
    common = rets.columns.intersection(w.index)
    rets_aligned = rets[common]
    w_aligned = w.loc[common]
    return rets_aligned, w_aligned, dd


def compute_metrics(rets: pd.DataFrame, weights: pd.Series, drawdown: pd.Series):
    port_ret = rets.dot(weights)
    ann_ret = (1 + port_ret).prod() ** (252 / len(port_ret)) - 1
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = ann_ret / ann_vol
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


def run_murphy(port_ret: pd.Series) -> dict:
    sims = simulate_murphy_risk(port_ret)
    stats = murphy_summary_stats(sims)
    return stats


def save_metrics(metrics: dict, output_path: Path) -> None:
    df = pd.DataFrame(metrics, index=[0]).T
    df.columns = ['Value']
    df.to_csv(output_path)
    logging.info(f"Metrics saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Portfolio metrics report with optional Murphy risk.")
    parser.add_argument('--returns', type=Path, default=Path('data/simple_returns.csv'), help='Path to returns CSV')
    parser.add_argument('--weights', type=Path, default=Path('data/optimized_weights.csv'), help='Path to weights CSV')
    parser.add_argument('--drawdown', type=Path, default=Path('data/portfolio_drawdown.csv'), help='Path to drawdown CSV')
    parser.add_argument('--output', type=Path, default=Path('data/metrics_summary.csv'), help='Output CSV for metrics')
    parser.add_argument('--murphy', action='store_true', help='Run Murphy Monte Carlo risk simulation')
    parser.add_argument(
    '--murphy',
    action='store_true',
    help='Run Monte Carlo Murphy Risk Simulation'
)
    
    args = parser.parse_args()

    setup_logger()
    logging.info("Metrics report started")

    rets, w, dd = load_data(args.returns, args.weights, args.drawdown)
    metrics = compute_metrics(rets, w, dd)

    if args.murphy:
        logging.info("Running Murphy Monte Carlo Simulation...")
        port_ret = rets.dot(w)
        murphy_stats = run_murphy(port_ret)
        for k, v in murphy_stats.items():
            metrics[f"Murphy {k}"] = v
        # Save Murphy metrics separately
        pd.DataFrame.from_dict(murphy_stats, orient='index', columns=['Value']).to_csv('data/murphy_metrics.csv')
        logging.info("Murphy metrics saved to data/murphy_metrics.csv")

    for k, v in metrics.items():
        logging.info(f"{k}: {v}")

    save_metrics(metrics, args.output)

if __name__ == '__main__':
    main()
