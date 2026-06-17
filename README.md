# 📊 Vectorized SMA Crossover Backtester

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange)

A vectorized backtesting and parameter-optimization framework in Python that searches for the most profitable **Simple Moving Average (SMA) crossover** strategy on the S&P 500 ETF (`SPY`), then validates the winner on held-out data to guard against overfitting.

The emphasis throughout is on **efficient, vectorized Pandas/NumPy operations** rather than slow row-by-row loops — returns, moving averages, and strategy performance are all computed on entire price series at once.

> This is the **research counterpart** to my live trading bot, [`alpaca-sma-trader`](https://github.com/EhsanDevv/alpaca-sma-trader). The 25/170 pair this backtester identified is the strategy that bot executes live (as a long-only adaptation).

---

## 🎯 What this project demonstrates

- **Vectorized time-series analysis** with Pandas/NumPy: log returns, cumulative returns, and rolling moving averages computed without iterative loops
- **Parameter optimization** via grid search across SMA window combinations
- **Sound validation methodology**: in-sample optimization on a training period and out-of-sample testing on a held-out period to detect overfitting
- **Performance benchmarking**: comparing a strategy's cumulative return against a buy-and-hold baseline
- **Market data acquisition** from a financial data API (`yfinance`)
- **Visualization** of results with Matplotlib

---

## ⚙️ How it works

**1. Data.** Pulls 5 years of daily `SPY` price data via `yfinance` and splits it chronologically: roughly the first 4 years as a training set and the final ~242 trading days (≈ 1 year) as an untouched out-of-sample test set.

**2. Feature engineering.** Computes daily **log returns** and **cumulative returns** on the training set using vectorized operations.

**3. Optimization (grid search).** Sweeps every combination of:

| Parameter | Range | Step | Values |
|---|---|---|---|
| Short SMA | 10 → 55 | 5 | 10 |
| Long SMA | 100 → 190 | 10 | 10 |

For each of the 100 pairs it builds a position signal (**long** when the short SMA is above the long SMA, **short** otherwise), applies it to the *next* day's returns to avoid look-ahead bias, and records the final cumulative strategy return. The pair with the highest in-sample return is selected.

**4. Out-of-sample test.** The winning pair is applied to the held-out final year. SMAs are computed over the full price series and then sliced to the test window, so the long moving average is valid from the first day of testing rather than needing a warm-up period — and because a rolling mean only looks backward, this introduces no look-ahead bias.

**5. Results.** Ranks the top-performing parameter pairs in a table and plots the out-of-sample strategy performance against a buy-and-hold benchmark with Matplotlib.

**Outcome:** the **25-day / 170-day** crossover emerged as the top in-sample performer and was carried forward into out-of-sample validation.

---

## 🛠️ Tech stack

- **Language:** Python 3.9+
- **Environment:** Jupyter Notebook
- **Libraries:** `pandas`, `numpy`, `yfinance`, `matplotlib`

---

## 🚀 Setup & usage

### 1. Clone and install
```bash
git clone https://github.com/EhsanDevv/sma-crossover-backtester.git
cd sma-crossover-backtester

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**`requirements.txt`**
```
pandas
numpy
yfinance
matplotlib
jupyter
```

### 2. Run
```bash
jupyter notebook SMA_Vectorized_Backtester.ipynb
```
Run the cells top to bottom. The notebook downloads the latest 5 years of `SPY` data at runtime, so exact figures will shift over time as new data arrives.

---

## 📁 Project structure
```
sma-crossover-backtester/
├── SMA_Vectorized_Backtester.ipynb   # Data, optimization, validation, visualization
├── requirements.txt
└── README.md
```

---

## 📈 Methodology notes

- **Strategy type.** The backtest models a **long/short** strategy (positions of +1 / −1). My live deployment uses a **long-only** adaptation to avoid the added risk of short-selling during sharp reversals.
- **No look-ahead bias.** Positions are shifted by one period before being applied to returns, so each day's trade uses only information available the day before.
- **Benchmark.** Strategy performance is measured against simple buy-and-hold of `SPY`.

---

## 🧭 Limitations & roadmap

A focused research project. Known limitations and where it could go next:

- **Return-only selection.** The optimal pair is chosen on cumulative return alone.
  *Planned: risk-adjusted metrics (Sharpe ratio, max drawdown) for more robust selection.*
- **No trading frictions.** Transaction costs and slippage are not modeled, which inflates apparent returns.
  *Planned: add a per-trade cost model.*
- **Single train/test split.** Validation uses one chronological holdout.
  *Planned: walk-forward analysis across multiple rolling windows for a sterner overfitting test.*
- **Single asset.** Tuned and tested only on `SPY`.
  *Planned: evaluate robustness across other tickers and regimes.*

---

## 📄 License

Released under the MIT License. See `LICENSE` for details.
