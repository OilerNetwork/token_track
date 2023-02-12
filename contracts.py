import ethereum
import addresses
import abis

oiler_token = ethereum.w3.eth.contract(address=addresses.oiler_token, abi=abis.oiler_token)
oiler_distribution = ethereum.w3.eth.contract(address=addresses.oiler_distribution, abi=abis.oiler_distribution)
uniswap_pool = ethereum.w3.eth.contract(address=addresses.oiler_uniswap_v2_pool, abi=abis.oiler_uniswap_v2_pool)