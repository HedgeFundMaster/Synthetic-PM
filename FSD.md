# 🧠 Trading Algo FSD  
### Synthetic PM Model (SPMM) — Functional Specification Document

---

### 💡 Core Mission:
Build an automated, extensible **portfolio construction and risk management engine** simulating a real-world hedge fund PM. It combines:

- 🧮 **Quantitative rigor** (MVO + Black–Litterman, alpha/beta metrics)
- ⚠️ **Risk defense** (drawdown analysis, Murphy’s Law framework)
- 📊 **Performance reporting** (Sharpe, Alpha, Beta, Max Drawdown, volatility)
- 🧠 **Conviction-weighted logic** to reweight/hedge based on signals

---

### 1. Introduction  
**Purpose:** Define design & requirements for Synthetic PM Model (SPMM), from ingestion to execution simulation.  
**Audience:** Quant PMs, researchers, engineers.

---

### 2. Scope  
- **Modular pipeline:**  
  `Data ingestion → Returns engine → Optimization → Macro logic → Risk monitoring → Execution simulation → Dashboard`  
- **MVP:** Local Streamlit interface → longer‑term: full web deployment

---

### 3. Terminology ✅
- **Universe:** List of tickers
- **Returns:** Simple & log
- **Optimizer:** Mean–variance & Black–Litterman
- **Macro Overlay:** Regime detection, event rules
- **Drawdown:** Peak-to-trough decline
- **Metrics:** Sharpe, Alpha, Beta, Max DD, annualized return/vol

---

### 4. Functional Requirements

#### 4.1 Data Layer ✅
- **FR1:** Upload/manage `tickers.csv`
- **FR2:** `fetch_data.py` — fetch adjusted closes from Yahoo Finance
- **FR3:** `compute_returns.py` → outputs `simple_returns.csv`, `log_returns.csv`

#### 4.2 Quant Engine 🧠 *(In Progress)*
- **FR4:** `optimize_portfolio.py` computes MVO weights
- **FR5:** `performance_metrics.py` → calculates alpha, beta, volatility, Sharpe
- **FR6a:** **Position limits & regularization**  
  - **FR6a.1:** Enforce no shorting (`w ≥ 0`)  
  - **FR6a.2:** Enforce max weight per asset (e.g. `w ≤ 20%`)  
  - **FR6a.3 (Optional):** L₂ regularization to smooth weight spikes
- **FR6b:** **Black–Litterman integration**  (research this tonight 1 hour)
  - Stub in `black_litterman_engine.py` for P, Q, τ views  
  - Blend BL expected returns/cov into optimizer
- **FR7:** `drawdown_analysis.py` → computes daily drawdown series + max drawdown
- **FR8:** `metrics_report.py` → aggregates KPIs: annualized return, volatility, Sharpe, alpha/beta, max drawdown

#### 4.3 Macro Overlay *(Upcoming)*
- **FR9:** Regime detection (`macro_overlay.py`) using indicators (e.g. VIX, CPI, yield curve)
- **FR10:** Event rule engine: map macro events to sector tilts
- **FR11:** Blend quant weights with macro tilts based on conviction factor

#### 4.4 Execution Simulator *(Week 4)*
- **FR12:** Simulate trades with slippage, transaction costs
- **FR13:** Log trades in CSV/DB
- **FR14:** Compute simulated P&L over time

#### 4.5 Visualization & UI *(Week 5)*
- **FR15:** Streamlit dashboard or similar  
  - Select universe, view prices & returns  
  - Display optimized weights & performance charts  
  - Scenario panel: adjust macro events & re-run

---

### 5. Non-Functional Requirements
- **NFR1:** Modular code organization under `/engine`
- **NFR2:** Robust logging, error handling
- **NFR3:** GitHub Actions CI for unit tests (e.g. test metrics functions)
- **NFR4:** Performance: data fetch <1 min for 1,000 tickers, optimization <30s

---

### 6. Timeline / Roadmap
| Week | Focus                                    | Status           |
|------|------------------------------------------|------------------|
| 1    | Data ingestion pipeline                  | ✅ Complete       |
| 2    | Returns engine & basic MVO optimizer     | ✅ Complete       |
| 3    | Macro overlay & blending logic           | 🟡 In progress    |
| 4    | Execution simulator & trade logging      | 🔜 Upcoming       |
| 5    | Streamlit UI & visualization             | 🔜 Upcoming       |
| 6    | Deployment, documentation, refactoring   | 🔜 Upcoming       |

---

### 7. Appendices
**A. Folder Structure**
```bash
Synthetic-PM/
├── engine/
│   ├── fetch_data.py
│   ├── compute_returns.py
│   ├── optimize_portfolio.py
│   ├── performance_metrics.py
│   ├── drawdown_analysis.py
│   ├── metrics_report.py
│   ├── black_litterman_engine.py  # soon
│   └── macro_overlay.py           # soon
├── data/
│   ├── tickers.csv
│   ├── price_data.csv
│   ├── simple_returns.csv
│   ├── optimized_weights.csv
│   ├── portfolio_drawdown.csv
│   └── metrics_summary.csv
├── tests/                         # add unit tests here
├── streamlit_app.py              # optional UI
├── FSD.md
├── README.md
├── requirements.txt
└── .gitignore
```

**B. Data Schema**
| File                      | Description                              |
|---------------------------|------------------------------------------|
| `simple_returns.csv`      | Daily returns matrix (dates × tickers)   |
| `optimized_weights.csv`   | Cleaned portfolio weights (ticker × w)   |
| `portfolio_drawdown.csv`  | Daily drawdown series                    |
| `metrics_summary.csv`     | One-row KPI snapshot                     |
| `views.csv`               | Black–Litterman views (ticker × view %)  |
```


