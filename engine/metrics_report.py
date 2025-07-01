import os
import argparse
import logging
import pandas as pd

def load_data(returns_path: str, weights_path: str):
    """
    Load return series and optimized weights, align tickers.
    Returns:
        rets_aligned (DataFrame): daily returns for common tickers
        w_aligned (Series): weights for common tickers
    """
    # Load returns
    rets = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    # Load weights
    w_df = pd.read_csv(weights_path, index_col=0)
    w = w_df.iloc[:, 0].dropna()

    # Align tickers
    common = rets.columns.intersection(w.index)
    missing = w.index.difference(common)
    extra = rets.columns.difference(common)
    if missing.any():
        logging.warning(f"Weights for tickers not in returns: {list(missing)}")
    if extra.any():
        logging.info(f"Returns for tickers not in weights will be ignored: {list(extra)}")
    return rets[common], w[common]


def compute_drawdown(port_cum: pd.Series) -> pd.Series:
    """
    Compute drawdown series from cumulative returns.
    """
    roll_max = port_cum.cummax()
    drawdown = (port_cum - roll_max) / roll_max
    return drawdown


def save_drawdown(drawdown: pd.Series, output_path: str):
    """
    Save drawdown series to CSV file.
    """
    df = drawdown.to_frame(name='Drawdown')
    df.to_csv(output_path)
    logging.info(f"Drawdown series saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Portfolio drawdown analysis.")
    parser.add_argument('--returns', default='data/simple_returns.csv', help='Path to returns CSV')
    parser.add_argument('--weights', default='data/optimized_weights.csv', help='Path to weights CSV')
    parser.add_argument('--output', default='data/portfolio_drawdown.csv', help='Output drawdown CSV')
    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    logging.info("Starting drawdown analysis...")

    # Load and align data
    rets_aligned, w_aligned = load_data(args.returns, args.weights)
    logging.info(f"Loaded returns ({rets_aligned.shape}) and weights ({len(w_aligned)} tickers)")

    # Compute portfolio cumulative returns
    port_ret = rets_aligned.dot(w_aligned)
    port_cum = (1 + port_ret).cumprod()
    logging.info(f"Final cumulative return: {port_cum.iloc[-1]:.4f}")

    # Compute and report max drawdown
    drawdown = compute_drawdown(port_cum)
    max_dd = drawdown.min()
    logging.info(f"Max drawdown: {max_dd:.2%}")

    # Save drawdown
    save_drawdown(drawdown, args.output)

if __name__ == "__main__":
    main()
