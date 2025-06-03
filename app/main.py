# app/main.py
from app.etl.extract import fetch_market_data
from app.etl.load import load_to_mongo

def main():
    print("Fetching data from CoinGecko...")
    data = fetch_market_data()
    print("Loading data into MongoDB...")
    load_to_mongo(data)
    print("Done.")

if __name__ == "__main__":
    main()
