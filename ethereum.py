import keys

from web3 import Web3
api_url = f"https://soft-crimson-field.discover.quiknode.pro/{keys.quick_node_key}/"
w3 = Web3(Web3.HTTPProvider(api_url))