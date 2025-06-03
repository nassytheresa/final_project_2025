from pycoingecko import CoinGeckoAPI

def fetch_market_data():
    cg = CoinGeckoAPI()
    data = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1)
    return data