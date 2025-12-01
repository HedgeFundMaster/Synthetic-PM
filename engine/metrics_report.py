#!/usr/bin/env python3

import argparse
import logging

import pandas as pd
import numpy as np

from murphy_risk_model import simulate_murphy_risk, murphy_summary_stats, plot_murphy_simulations


def setup_logger() -> None:
    """Configure root logger for consistent formatting."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_data(returns_path: str, weights_path: str, drawdown_path: str):
    """
    Load and align returns, weights, and drawdown series.
    Returns:
        rets (DataFrame), weights (Series), drawdown (Series)
    """
    rets = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    w_df = pd.read_csv(weights_path, index_col=0, header=None)
    weights = w_df.iloc[:, 0]
    dd = pd.read_csv(drawdown_path, index_col=0, parse_dates=True).iloc[:, 0]
    common = rets.columns.intersection(weights.index)
    return rets[common], weights.loc[common], dd


def compute_metrics(rets: pd.DataFrame, weights: pd.Series, drawdown: pd.Series) -> dict:
    """
    Compute portfolio analytics: return, vol, Sharpe, beta, alpha, max drawdown.
    """
    port_ret = rets.dot(weights)
    # Annualized return & vol
    ann_ret = (1 + port_ret).prod() ** (252 / len(port_ret)) - 1
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = ann_ret / ann_vol
    # Beta & alpha via numpy.polyfit
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
        'Max Drawdown': max_dd
    }


def save_metrics(metrics: dict, output_path: str) -> None:
    df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
    df.to_csv(output_path)
    logging.info(f"Metrics saved to {output_path}")


def run_murphy(port_ret: pd.Series) -> None:
    logging.info("Running Murphy Monte Carlo Simulation...")
    sims = simulate_murphy_risk(port_ret)
    plot_murphy_simulations(sims)
    stats = murphy_summary_stats(sims)
    for k, v in stats.items():
        logging.info(f"Murphy {k}: {v:.4f}")
    pd.DataFrame.from_dict(stats, orient='index', columns=['Value']).to_csv('data/murphy_summary.csv')
    logging.info("Murphy metrics saved to data/murphy_summary.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Portfolio metrics report")
    parser.add_argument('--returns', default='data/simple_returns.csv', help='Path to returns CSV')
    parser.add_argument('--weights', default='data/optimized_weights.csv', help='Path to weights CSV')
    parser.add_argument('--drawdown', default='data/portfolio_drawdown.csv', help='Path to drawdown CSV')
    parser.add_argument('--output', default='data/metrics_summary.csv', help='Output CSV for metrics')
    parser.add_argument('--murphy', action='store_true', help='Run Monte Carlo Murphy Risk Simulation')
    args = parser.parse_args()

    setup_logger()
    logging.info("Metrics report started")

    rets, weights, drawdown = load_data(args.returns, args.weights, args.drawdown)
    metrics = compute_metrics(rets, weights, drawdown)
    for k, v in metrics.items():
        logging.info(f"{k}: {v:.4f}")
    save_metrics(metrics, args.output)

    if args.murphy:
        port_ret = rets.dot(weights)
        run_murphy(port_ret)


if __name__ == '__main__':
    main()



