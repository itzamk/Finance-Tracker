# coingecko.py
import requests
import json

def fetch_assets():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve assets: {response.status_code}")
        return None

def fetch_price(crypto_id):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd'
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        if crypto_id in response_data and 'usd' in response_data[crypto_id]:
            return response_data[crypto_id]['usd']
        else:
            print(f'No price data found for {crypto_id}')
            return None
    else:
        print(f'Failed to retrieve price data: {response.status_code}')
        return None

def fetch_asset_info(asset_id):
    # Fetch the asset info using the asset_id
    url = f'https://api.coingecko.com/api/v3/coins/{asset_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if 'usd' key exists before accessing it
        usd_price = data['market_data']['current_price'].get('usd', 'N/A')
        # Extract and return the relevant information
        return {
            'name': data['name'],
            'ticker': data['symbol'].upper(),
            'price': usd_price,
            # ???
        }
    else:
        print(f'Failed to retrieve asset info: {response.status_code}')
        return None
    
def fetch_price_history(crypto_id, days='7', interval='daily'):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}&interval={interval}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to retrieve price history: {response.status_code}')
        return None
