import requests


# Coin aliases for user-friendly input
coin_aliases = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ltc": "litecoin",
    "doge": "dogecoin",
    "bnb": "binancecoin",
    "xrp": "ripple",
    "ada": "cardano",
    "dot": "polkadot",
    "sol": "solana",
    "matic": "matic-network"
}

def function_tool(name=None):
    def decorator(func):
        func._is_tool = True
        func._tool_name = name or func.__name__
        return func
    return decorator

@function_tool("get_crypto_price")
def get_crypto_price(coin: str = "bitcoin", currency: str = "usd") -> str:
    coin_id = coin_aliases.get(coin.lower(), coin.lower())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    response = requests.get(url)

    if response.status_code != 200:
        return f"❌ Failed to fetch price for {coin} to {currency}"

    data = response.json()
    try:
        price = data[coin_id][currency.lower()]
        return f"The current price of {coin.upper()} is {price} {currency.upper()}."
    except KeyError:
        return f"❌ Invalid coin or currency: {coin} to {currency}"
