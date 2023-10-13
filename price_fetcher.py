'''from coinbase.wallet.client import Client

def get_current_price(asset_name):
    # Initialize the Coinbase client (no authentication needed for this endpoint)
    client = Client(api_key='', api_secret='')
    
    # Make the API request to get the spot price
    try:
        currency_pair = f'{asset_name}-USD'  # Assume all assets are priced in USD
        price_info = client.get_spot_price(currency_pair=currency_pair)
        return float(price_info.amount)
    
    except Exception as e:
        print(f"Failed to fetch price for {asset_name}: {e}")
        return None'''

def get_current_price(asset_name):
    return float(100)