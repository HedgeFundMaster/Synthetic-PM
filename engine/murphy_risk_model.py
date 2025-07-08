import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate_murphy_risk(
    portfolio_returns: pd.Series,
    n_simulations: int = 5_000,
    n_days: int = 252,
    shock_probability: float = 0.02,
    shock_magnitude: float = -0.20,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Run Monte Carlo simulations where each day returns normally but
    occasionally suffers a Murphy “shock” drop.
    """
    np.random.seed(seed)
    daily_drift = portfolio_returns.mean()
    daily_vol   = portfolio_returns.std()
    # build an array (n_days x n_simulations)
    sims = np.zeros((n_days, n_simulations))

    for sim in range(n_simulations):
        # start at 1.0 (100% of initial capital)
        price_path = [1.0]
        for day in range(1, n_days):
            r = np.random.normal(daily_drift, daily_vol)
            # maybe a shock?
            if np.random.rand() < shock_probability:
                r += shock_magnitude
            price_path.append(price_path[-1] * (1 + r))
        sims[:, sim] = price_path

    # turn into DataFrame with date index if you like:
    return pd.DataFrame(sims)

def murphy_summary_stats(simulated_paths: pd.DataFrame) -> dict:
    """
    Compute summary stats across all simulated paths:
    - expected terminal value, VaR, expected drawdown, etc.
    """
    terminal_values = simulated_paths.iloc[-1, :]
    exp_term = terminal_values.mean()
    var_5pct = np.percentile(terminal_values, 5)
    max_dd    = (simulated_paths.cummax() - simulated_paths).max().max()
    return {
        "Expected Terminal Value": exp_term,
        "5% VaR": var_5pct,
        "Worst Drawdown": max_dd,
    }

def plot_murphy_simulations(
    simulated_paths: pd.DataFrame,
    n_show: int = 100,
    figsize: tuple = (12, 6),
) -> None:
    """Plot a subset of simulation paths."""
    plt.figure(figsize=figsize)
    for i in range(min(n_show, simulated_paths.shape[1])):
        plt.plot(simulated_paths.iloc[:, i], alpha=0.1, color="blue")
    plt.title(f"{simulated_paths.shape[1]} Murphy Simulations")
    plt.xlabel("Days")
    plt.ylabel("Portfolio Value")
    plt.show()

