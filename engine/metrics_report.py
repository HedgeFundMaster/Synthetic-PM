import argparse
import logging
import pandas as pd
import numpy as np


def load_data(returns_path: str, weights_path: str, drawdown_path: str):
    """
    Load returns, weights, and drawdown series; align tickers.
    Returns:
        rets_aligned (pd.DataFrame), w_aligned (pd.Series), drawdown (pd.Series)
    """
    # Load returns
    rets = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    # Load weights
    w_df = pd.read_csv(weights_path, index_col=0)
    w = w_df.iloc[:, 0]
    # Load drawdown
    dd = pd.read_csv(drawdown_path, index_col=0, parse_dates=True).iloc[:, 0]
    # Align tickers between returns and weights
    common = rets.columns.intersection(w.index)
    rets_aligned = rets[common]
    w_aligned = w.loc[common]
    return rets_aligned, w_aligned, dd


def compute_metrics(rets: pd.DataFrame, weights: pd.Series, drawdown: pd.Series):
    """
    Compute performance metrics: annualized return, volatility, Sharpe, beta, alpha, max drawdown.
    Returns:
        dict of metrics
    """
    # Portfolio returns
    port_ret = rets.dot(weights)
    # Annualized return & vol
    ann_ret = (1 + port_ret).prod() ** (252 / len(port_ret)) - 1
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = ann_ret / ann_vol
    # Beta & alpha via numpy.polyfit
    # Use benchmark as equally weighted market proxy if lacking SPY
    if 'SPY' in rets.columns:
        bench_ret = rets['SPY']
    else:
        bench_ret = rets.mean(axis=1)
    df = pd.concat([port_ret.rename('Portfolio'), bench_ret.rename('Benchmark')], axis=1).dropna()
    beta, alpha_daily = np.polyfit(df['Benchmark'], df['Portfolio'], 1)
    alpha_ann = alpha_daily * 252
    # Max drawdown
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


def save_metrics(metrics: dict, output_path: str):
    df = pd.DataFrame(metrics, index=[0]).T
    df.columns = ['Value']
    df.to_csv(output_path)
    logging.info(f"Metrics saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Portfolio metrics report")
    parser.add_argument('--returns', default='data/simple_returns.csv')
    parser.add_argument('--weights', default='data/optimized_weights.csv')
    parser.add_argument('--drawdown', default='data/portfolio_drawdown.csv')
    parser.add_argument('--output', default='data/metrics_summary.csv')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logging.info("Metrics report started")

    rets, w, dd = load_data(args.returns, args.weights, args.drawdown)
    metrics = compute_metrics(rets, w, dd)
    for k, v in metrics.items():
        logging.info(f"{k}: {v}")
    save_metrics(metrics, args.output)

if __name__ == '__main__':
    main()

