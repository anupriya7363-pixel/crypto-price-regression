# Crypto Price Regression: BTC vs ETH

Simple linear regression to predict Ethereum price from Bitcoin price,
using daily data fetched from the CoinGecko API.

## Setup
1. `python -m venv venv` and activate it
2. `pip install -r requirements.txt`
3. Create a `.env` file with `COINGECKO_API_KEY=your_key`
4. `python src/fetch_data.py`

## Status
Data fetching done. EDA and modelling in progress.s

## Results
| Model | Test R2 | Test MAE |
|---|---|---|
| A: BTC -> ETH (price) | 0.923 | $75.6 |
| B: days -> ETH (baseline) | -13.40 | $1137.8 |
| C: BTC return -> ETH return | 0.749 | - |

## Key learnings
- BTC price explains most of ETH price (test R2 0.92); a time-only baseline fails badly (negative R2), because the trend does not carry into the test period.
- The relationship holds on daily returns too (test R2 0.75, beta 1.30): ETH moves ~1.3% per 1% BTC move.
- Train R2 > test R2 in both cases, as expected with a time-based split.

## Limitations
- Same-day relationship, not a forecast of future prices
- One feature, one year of data, ~73-day test window
- Crypto relationships change over time. Not financial advice