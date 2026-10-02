import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COINGECKO_API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"
ROOT = Path(__file__).resolve().parent.parent


def fetch_prices(coin_id, days=365, retries=4):
    """Ek coin ka daily USD price fetch karke DataFrame (date, price) return karta hai."""
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    headers = {"x-cg-demo-api-key": API_KEY} if API_KEY else {}

    for attempt in range(retries):
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if response.status_code in (401, 429):  # demo API kabhi rate limit pe 401 deta hai
            print(f"{coin_id}: status {response.status_code}, retry {attempt + 1}...")
            time.sleep(20 * (attempt + 1))
            continue
        response.raise_for_status()

        df = pd.DataFrame(response.json()["prices"], columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.normalize()
        # last row kabhi duplicate date hoti hai, isliye har date ka last price rakho
        return df.groupby("date", as_index=False)["price"].last()

    raise RuntimeError(f"{coin_id}: rate limit ke karan fetch fail hua")


def main():
    btc = fetch_prices("bitcoin").rename(columns={"price": "btc_price"})
    time.sleep(15)  # API ko saans lene do
    eth = fetch_prices("ethereum").rename(columns={"price": "eth_price"})

    df = btc.merge(eth, on="date", how="inner").sort_values("date")

    out = ROOT / "data" / "raw.csv"
    out.parent.mkdir(exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows -> {out}")
    print(df.head())


if __name__ == "__main__":
    main()