import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate_murphy_risk(
    portfolio_returns: pd.Series,
    n_simulations: int = 5000,
    n_days: int = 252,
    shock_probability: float = 0.02,
    shock_magnitude: float = -0.20,
    seed: int = 42
) -> pd.DataFrame:
    # ... (your Monte Carlo function) …

def murphy_summary_stats(simulated_paths: pd.DataFrame) -> dict:
    # ... (your summary stats function) …

def plot_murphy_simulations(simulated_paths: pd.DataFrame, n_show: int = 100):
    # ... (your plotting function) …
