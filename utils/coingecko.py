import requests

def get_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        'name': data['name'],
        'symbol': data['symbol'],
        'current_price': data['market_data']['current_price']['usd'],
        'price_change_percentage_24h': data['market_data']['price_change_percentage_24h'],
        'market_cap': data['market_data']['market_cap']['usd'],
        'total_supply': data['market_data']['total_supply']
    }

def get_coin_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[coin_id]['usd']

def get_coin_history(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['prices']


COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'

def get_coin_id(coin_name):
    response = requests.get(f"{COINGECKO_API_URL}/coins/list")
    if response.status_code == 200:
        coins = response.json()
        for coin in coins:
            if coin_name.lower() == coin['id'] or coin_name.lower() == coin['symbol']:
                return coin['id']
    return None

def get_historical_data(coin_id, days):
    url = f"{COINGECKO_API_URL}/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": response.status_code, "message": response.text}