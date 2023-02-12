import logging
import ethereum
import addresses
import abis
import contracts

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# block = w3.eth.getBlock('latest') # get latest block details
# block_alt = w3.eth.blockNumber # get latest block number

oiler_token_name = 'Oiler' # oiler_token_contract.functions.name().call()
oiler_token_symbol = 'OIL' # oiler_token_contract.functions.symbol().call()
print('token address:                 ' + addresses.oiler_token)
print('token name:                    ' + oiler_token_name)
print('token symbol:                  ' + oiler_token_symbol)
print('distribution address:          ' + addresses.oiler_distribution)
print('private distribution address:  ' + addresses.oiler_private_distribution)
print('advisors distribution address: ' + addresses.oiler_advisors_distribution)

# print some totals
oiler_decimals = 18 # contracts.oiler_token.functions.decimals().call()
oiler_total_supply = 100_000_000_000_000_000_000_000_000 # contracts.oiler_token.functions.totalSupply().call()
print('decimals:                      ' + str(oiler_decimals))
print('total supply:                  ' + f"{oiler_total_supply:,}")
print('total supply std:              ' + f"{int(oiler_total_supply / 10**oiler_decimals):,}")

# now get all token holders, order them, display some statistics
# https://web3py.readthedocs.io/en/v5/examples.html#advanced-example-fetching-all-token-transfer-events
# logging.debug("Debug message")
# logging.info("Info message")
# logging.warning("Warning message")
# logging.error("Error message")

# check the unclaimed tokens in various distributions, check the claimable and locked values

# here are the allowances for team
# https://revoke.cash/address/0xeaab5ec0f9dc67d9e2810c02117abb33537a68d8