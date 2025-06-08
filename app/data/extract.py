from pycoingecko import CoinGeckoAPI
from app.data.store import store_to_mongo
import time


def fetch_market_data(
    currency: str = "usd",
    order: str = "market_cap_desc",
    per_page: int = 10,
    page: int = 1,
):
    """Fetch market data from CoinGecko

    Args:
        currency (str, optional): Currency to fetch data in. Defaults to "usd".
        order (str, optional): Order by which to sort the data. Defaults to "market_cap_desc".
        per_page (int, optional): Number of items per page. Defaults to 10.
        page (int, optional): Page number. Defaults to 1.

    Returns:
        list[dict]: List of market data
    """
    cg = CoinGeckoAPI()
    data = cg.get_coins_markets(
        vs_currency=currency, order=order, per_page=per_page, page=page
    )
    return data


def fetch_and_store_data(pages: int = 10, per_page: int = 100, delay: int = 1):
    """
    Fetch cryptocurrency data from CoinGecko and store in MongoDB.

    Args:
        pages: Number of pages to fetch
        per_page: Number of items per page
        delay: Delay between requests in seconds
    """
    print("Fetching data from CoinGecko...")
    for page in range(pages):
        data = fetch_market_data(page=page + 1, per_page=per_page)
        print(f"Page {page + 1} fetched {len(data)} rows")
        store_to_mongo(data)
        time.sleep(delay)

    print("Data fetching and storage completed.")
