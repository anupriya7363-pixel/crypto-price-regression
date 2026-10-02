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