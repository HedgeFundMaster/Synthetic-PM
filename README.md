# Synthetic-PM
Synthetic PM Model (SPMM), blending systematic signals with real-world geopolitical/macro insight.
# Current Thesis 
Markets are not merely stochastic systems, but  historical artifacts shaped by narratives, institutions, and regime memory. By integrating a historian’s interpretive lens into quantitative modeling, this SPMM seeks to go beyond alpha decay and uncover persistent structural advantages rooted in cyclical and geopolitical pattern recognition.

# 🧠 Synthetic Portfolio Management Model (SPMM): Scientific Method + Strategy Memo

Brendan O’Sullivan — July 2025

---

## 📍 Project Direction Statement

This project will extend beyond August 10th. As I deepen my research, get pushback, and continue to learn, I realize that the real edge in this SPMM lies in **discovering a differentiated signal**—one that fuses historical thinking with systematic modeling. Alpha won’t come from copying quant templates; it will come from interpreting market behavior as **deeply historical**, path-dependent, and narrative-sensitive. That’s the foundation of my edge.

---

## 📊 Scientific Method Framework 

#1. Observation

* Traditional quant models focus on short-term statistical patterns, assuming return distributions are mostly stationary.
* But market regimes are shaped by history: wars, political cycles, liquidity changes, and policy shifts often follow recognizable trajectories.
* Investors do not interpret information in a vacuum—they interpret it through *memory* and *historical analogy*.

#  2. Question

> Can incorporating historical regime archetypes and interpretive signals into a quantitative portfolio model enhance robustness and deliver alpha beyond traditional factor-based methods?

### 3. Hypothesis

> If present-day macro and volatility data resemble historically significant regimes, then we can proactively tilt the portfolio to align with historical outcomes. This may yield excess risk-adjusted returns, especially in crisis scenarios or slow-moving regime shifts.

### 4. Background Research

* Quantitative Base (Ongoing):

  * AQR – Alpha Beyond Expected Returns
  * PyPortfolioOpt, Sharpe optimization
  * Historical + Structural Thinking (Ongoing):

  * Ray Dalio – *Big Debt Crises*
  * Fernand Braudel – *Time structures* (event, conjuncture, longue durée)
  * Kondratiev Waves, Toynbee, Turchin, Napier
* Behavioral + Narrative Components:

  * Path dependence
  * Regime memory (e.g., 2008 PTSD)
  * Cochrane's warning: *"Easy money in finance is a myth—test every edge deeply."*

#5. Methodology

# a. Data Layer

* `price_data.csv`, `macro_indicators.csv`, `optimized_weights.csv`
* Future: real-time data via Polygon or Alpaca

# b. Quant Layer

* Run optimization using PyPortfolioOpt
* Max Sharpe ratio portfolio under constraints
* Traditional factors: momentum, volatility, beta

# c. Historical Regime Classification Layer

* Tag environment using rules:

  * “Stagflation”: CPI YoY > 4%, VIX > 25 → overweight real assets
  * “Tech Bubble”: negative earnings + rapid multiple expansion → cut growth beta
* Use macro tags to create a "Regime Similarity Index"

#### d. **Macro Overlay Layer**

* Tilt weights based on tagged regimes (via `macro_overlay.py`)
* Simulate the difference in behavior under different historical analogies

#### e. Risk Testing (Murphy Module)

* Monte Carlo: 5000 paths, 252 days
* Inject 2% probability tail shocks (e.g., -20%)
* Visualize fat-tail distributions and regime-resilience

#### f. Evaluation Layer

* Output from `metrics_report.py`

  * Sharpe, Alpha, Max Drawdown, VaR, Skew
* Compare regime-aware model vs. static model

---

# 6. Results

* Compare optimizer with/without historical regime tagging
* Track changes in tail loss containment, alpha persistence, Sharpe stability
* Evaluate against EMH blind spots (see below)

---

## 🧠 Integrating Efficient Market Hypothesis (EMH)

# 🔍 Why Understanding EMH Sharpens This Model

Fama’s Efficient Market Hypothesis claims:

> “Prices reflect all available information.”

But…

|     EMH Form    |       What It Misses                    |                     My Edge                             |
| --------------- | --------------------------------------- | ------------------------------------------------------- |
| Weak            | Can’t explain momentum                  |       You can detect regime transition signals          |
| Semi-Strong     | Ignores *interpretation* of public info | Investors misread macro context                         |
| Strong          | Assumes no behavioral distortion        | Fear, memory, and narratives distort capital allocation |

# Conclusion:
My model does not reject EMH. It finds alpha where EMH is weakest*, in how historical memory, narrative lag, and institutional friction cause markets to misclassify the meaning** of data.

---

# 📜 Strategic Roadmap: SPMM Level Progression

| Level       | Description                                  | Status         |
| ----------- | -------------------------------------------- | -------------- |
| 🟩 Level 1  | Basic model, optimizer, metrics, Murphy risk | ✅ Complete     |
| 🟨 Level 2  | Regime classifier, historical overlays       | 🚧 In Progress |
| 🟧 Level 3  | Publishable alpha thesis, narrative signals  | 🔜 Upcoming    |
| 🟥 Level 4  | Execution simulation, portfolio dashboard    | 🔒 Future      |
| 🏋️ Level ∞ | Brendan’s branded framework                  | 🔭 Your legacy |

---

# 🧠 Working Thesis

> Markets are efficient at processing data but inefficient at interpreting history. The Synthetic PMM exploits this gap by fusing quant logic with regime-aware historical mapping, creating a system designed not to predict the future, but to better understand when the past is repeating itself in rhyme.
