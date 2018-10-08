import json

def get_wallets_fn(f_json):
    def get_wallets(_):
        with open(f'test/fb_data/{f_json}.json', 'r') as f_wallets:
            return json.load(f_wallets)
    return get_wallets
