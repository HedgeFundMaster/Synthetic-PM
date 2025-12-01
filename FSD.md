# 🧠 Synthetic PMM Functional Specification Document (FSD)

## 🔄 Version
**v2.2** – Last updated: November 30, 2025

---

## 📌 Objective
Build a real-time Synthetic Portfolio Management Model (SPMM) that mimics the discretionary and systematic workflows of hedge fund PMs using quant signals, macro overlays, risk modeling, and AI.

---

## 🧱 System Architecture Overview

```
                    +-------------------+
                    |  Market + Macro   |
                    |    Data Feeds     |
                    +-------------------+
                              |
                              v
+-----------+       +-------------------+       +----------------+       +-------------+
| price_data|-----> |  Optimizer Engine |-----> | Portfolio Weights |---> | Execution Sim |
+-----------+       +-------------------+       +----------------+       +-------------+
                              |
                              v
                    +-------------------+
                    | Performance Engine |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    | Murphy Risk Module |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    |  Metrics + Reports |
                    +-------------------+
```

---

## ✅ Core Modules

### 1. **Optimizer Engine**
- File: `optimize_portfolio.py`
- Libraries: PyPortfolioOpt
- Inputs: `price_data.csv`
- Logic:
  - Compute expected returns + sample covariance
  - Optimize for max Sharpe ratio
  - Clean weights
  - Output to: `optimized_weights.csv`
- ✅ Now includes constraint logic (max weight per asset)

---

### 2. **Performance Metrics Engine**
- File: `metrics_report.py`
- Inputs: `simple_returns.csv`, `optimized_weights.csv`, `portfolio_drawdown.csv`
- Outputs: `metrics_summary.csv`
- Metrics Tracked:
  - Annualized Return
  - Volatility
  - Sharpe Ratio
  - Beta
  - Alpha
  - Max Drawdown
- ✅ Confirmed clean end-to-end execution

---

### 3. **Murphy Risk Module**
- File: `murphy_risk_model.py` + `murphy_report.py`
- Purpose: Simulates tail risk events & portfolio resilience under rare shocks (e.g. 20% crash days)
- Simulation Type: Monte Carlo
- Key Params:
  - 5000 Simulations
  - 252 Days
  - 2% shock probability
  - -20% shock magnitude
- Outputs:
  - Simulated return paths
  - Plot of outcomes
  - Summary stats: Worst Case Return, VaR, Skew, etc.
- 🔧 Next: Add `.csv` output for Murphy summary metrics

---

### 4. **Macro Overlay Engine**
- File: `macro_overlay.py`
- Status: Scaffolded
- Logic in progress:
  - If VIX > 25 → reduce cyclicals
  - If CPI YoY > 4% → tilt toward real assets
  - Can adjust optimizer weights dynamically
- Input: Mock `macro_indicators.csv` for now

---

### 5. **Development Notebook (New)**
- File: `SPMM_dev_lab.ipynb`
- Purpose:
  - Interactive experimentation
  - Simulations + visualizations
  - Easy parameter tuning for Murphy and Optimizer
- Run via VS Code’s Jupyter environment
- Kernel: Use project virtual environment
- Useful for:
  - Debugging
  - Visual testing
  - Future: Macroeconomic blending visual UI

---

## 🔮 Next Phase Modules

### 🔜 Black–Litterman Engine
- File: `black_litterman_engine.py`
- Goal: Incorporate subjective macro views into optimization
- Logic:
  - Read `views.csv` (e.g. META expected to outperform SPY by 3%)
  - Blend with priors using B-L formula
  - Output new expected returns → pass to optimizer
- Status: Not started (Week 4 priority)

### 🔬 Physics Risk Engine (Future Edge)
- Entropy, liquidity modeling, non-linear shock chains
- Inspired by Farther, Point72, and QIS frameworks
- Will layer on top of Murphy module

---

## 📄 Other Docs
- `README.md` – Top-level project instructions
- `requirements.txt` – All current Python dependencies
- `.gitignore` – Keeps data + secrets out of Git

---

## 📅 Completion Timeline

| Week | Focus                                  | Status      |
|------|----------------------------------------|-------------|
| 1    | Data ingestion, returns, drawdowns     | ✅ Complete |
| 2    | Optimizer + metrics engine             | ✅ Complete |
| 3    | Murphy risk + macro overlay            | 🔄 In Progress |
| 4    | Black–Litterman integration            | ⏳ Next     |
| 5    | Physics-based logic + risk sims        | 🔒 Planned  |
| 6    | UI, deployment polish                  | 🔒 Planned  |

---




