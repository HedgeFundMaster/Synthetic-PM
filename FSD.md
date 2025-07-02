Absolutely, Brendan. Here's your updated **FSD** with the **Drawdown Analysis**, **Metrics Module**, and pending **Black-Litterman integration** folded in cleanly. Copy-paste ready for Notion:

---

# 🧠 Trading Algo FSD

### Synthetic PM Model (SPMM) — Functional Specification Document

---

### 💡 Core Mission:

Build an automated, extensible **portfolio construction and risk management engine** simulating a real-world hedge fund PM. It combines:

* 🧮 **Quantitative rigor** (MVO + Black-Litterman, alpha/beta metrics)
* ⚠️ **Risk defense** (drawdown analysis, Murphy’s Law framework)
* 📊 **Performance reporting** (Sharpe, Alpha, Beta, Max Drawdown, volatility)
* 🧠 **Conviction-weighted logic** to reweight/hedge based on signals

---

### 1. Introduction

**Purpose:** Define design & requirements for Synthetic PM Model (SPMM), from ingestion to execution sim.
**Audience:** Quant PMs, researchers, engineers.

---

### 2. Scope

* Modular pipeline:
  `Data ingestion → Returns engine → Optimization → Macro logic → Risk → Execution → Dashboard`
* MVP: Local Streamlit interface → long-term: full web deployment

---

### 3. Terminology ✅

* **Universe**: List of tickers
* **Returns**: Simple & log
* **Optimizer**: Mean–variance & Black–Litterman
* **Macro Overlay**: Regime detection, event response
* **Drawdown**: Peak-to-trough decline
* **Metrics**: Sharpe, Alpha, Beta, Max DD

---

### 4. Functional Requirements

#### 4.1 Data Layer ✅

* **FR1**: Upload/manage `tickers.csv`
* **FR2**: `fetch_data.py` — fetch adj. closes from Yahoo Finance
* **FR3**: `compute_returns.py` → outputs `simple_returns.csv`, `log_returns.csv`

#### 4.2 Quant Engine 🧠 *(In Progress)*

* **FR4**: `optimize_portfolio.py` computes MVO weights
* **FR5**: `performance_metrics.py` → calculates **alpha**, **beta**
* **FR6**: `black_litterman_engine.py` (🆕) — adds conviction views + implied returns

  * Supports: `P`, `Q`, and `tau` matrices
  * Can override or blend with MVO
* **FR7**: `drawdown_analysis.py` → computes rolling drawdown series
* **FR8**: `metrics_report.py` → annualized return, vol, Sharpe, max drawdown

#### 4.3 Macro Overlay *(Coming Week 3)*

* **FR9**: Regime detection engine (VIX, CPI, yield curve slope)
* **FR10**: Event rule engine (e.g., "Fed hike" = overweight banks)
* **FR11**: Blend macro tilts with quant weights via `conviction_score`

#### 4.4 Execution Simulator *(Week 4)*

* **FR12**: Simulate trades with slippage, delays
* **FR13**: Log trades in CSV or DB table
* **FR14**: Calculate simulated portfolio P\&L

#### 4.5 Visualization & UI *(Week 5)*

* **FR15**: Streamlit dashboard

  * Load tickers, visualize price & return data
  * Show optimized weights, risk metrics
  * Adjust macro views, re-run portfolio

---

### 5. Non-Functional Requirements

* **NFR1**: Modular structure under `/engine`
* **NFR2**: Robust logging + error handling
* **NFR3**: GitHub source control + GitHub Actions for CI (unit test core metrics)
* **NFR4**: Performance: data pull < 1 min, optimization < 30s for ≤ 1,000 tickers

---

### 6. Timeline / Roadmap

| Week | Focus                                   | Status         |
| ---- | --------------------------------------- | -------------- |
| 1    | Data ingestion pipeline                 | ✅ Complete     |
| 2    | Returns + MVO optimization + metrics    | 🟡 In progress |
| 3    | Macro regime detection + event overlays | ⏳ Upcoming     |
| 4    | Execution simulator & trade logging     | ⏳ Upcoming     |
| 5    | Streamlit UI + Visualization            | ⏳ Upcoming     |
| 6    | Deployment, Documentation, Refactor     | ⏳ Upcoming     |

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
│   └── black_litterman_engine.py (🆕 Soon)
├── data/
│   ├── tickers.csv
│   ├── simple_returns.csv
│   ├── optimized_weights.csv
│   ├── portfolio_drawdown.csv
│   └── metrics_summary.csv
```

**B. Data Schema**

| File                     | Description                     |
| ------------------------ | ------------------------------- |
| `simple_returns.csv`     | Daily return series for tickers |
| `optimized_weights.csv`  | Optimized weight vector         |
| `portfolio_drawdown.csv` | Daily drawdown series           |
| `metrics_summary.csv`    | Final performance metrics       |
| `tickers.csv`            | Initial universe of assets      |

---

