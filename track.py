import logging
import ethereum
import addresses
import abis
import contracts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# block = w3.eth.getBlock('latest') # get latest block details
# block_alt = w3.eth.blockNumber # get latest block number

just_length = 32
oiler_token_name = 'Oiler' # oiler_token_contract.functions.name().call()
oiler_token_symbol = 'OIL' # oiler_token_contract.functions.symbol().call()
print('token address:                  '.ljust(just_length) + addresses.oiler_token)
print('token name:                     '.ljust(just_length) + oiler_token_name)
print('token symbol:                   '.ljust(just_length) + oiler_token_symbol)
print('distribution address:           '.ljust(just_length) + addresses.oiler_distribution)
print('private distribution address:   '.ljust(just_length) + addresses.oiler_private_distribution)
print('advisors distribution address:  '.ljust(just_length) + addresses.oiler_advisors_distribution)

# print some totals
oiler_decimals = 18 # contracts.oiler_token.functions.decimals().call()
oiler_total_supply = 100_000_000_000_000_000_000_000_000 # contracts.oiler_token.functions.totalSupply().call()

def normalize(amount):
    return int(amount / 10**oiler_decimals)

def format_amount(amount):
    return f"{normalize(amount):,}"
    
print('decimals:                       ' + str(oiler_decimals))
print('total supply:                   ' + f"{oiler_total_supply:,}")
print('total supply std:               ' + format_amount(oiler_total_supply))

# now get all token holders, order them, display some statistics
# https://web3py.readthedocs.io/en/v5/examples.html#advanced-example-fetching-all-token-transfer-events
# logging.debug("Debug message")
# logging.info("Info message")
# logging.warning("Warning message")
# logging.error("Error message")

# check the unclaimed tokens in various distributions, check the claimable and locked values

# here are the allowances for team
# https://revoke.cash/address/0xeaab5ec0f9dc67d9e2810c02117abb33537a68d8

# mappping of distributions

ADVISORS_REWARD = 4
ECOSYSTEM_FUND = 1
FOUNDATION_REWARD = 5
LIQUIDITY_FUND = 6
PRIVATE_OFFERING = 3
TEAM_FUND = 2

distributions = {
    ADVISORS_REWARD:    ["advisors", addresses.oiler_advisors_distribution],
    ECOSYSTEM_FUND:     ["ecosystem", addresses.oiler_ecosystem_distribution],
    FOUNDATION_REWARD:  ["foundation", addresses.oiler_foundation_distribution],
    LIQUIDITY_FUND:     ["liquidity", addresses.oiler_liquidity_distribution],
    PRIVATE_OFFERING:   ["private", addresses.oiler_private_distribution],
    TEAM_FUND:          ["team", addresses.oiler_team_distribution],
}

for key in distributions:
    stake = contracts.oiler_distribution.functions.stake(key).call()
    left = contracts.oiler_distribution.functions.tokensLeft(key).call()
    balance = contracts.oiler_token.functions.balanceOf(distributions[key][1]).call()
    transferred = stake - left - balance
    print(f"{distributions[key][0]}: ".ljust(just_length) + f"{format_amount(balance)}".rjust(11) + " + " + f"{format_amount(left)}".rjust(11) + " / " + f"{format_amount(stake)}".rjust(11) + " -> " + f"{format_amount(transferred)}".rjust(11) + " transferred")

uniswap_balance = contracts.oiler_token.functions.balanceOf(addresses.oiler_uniswap_v2_pool).call()
print(f"uniswap balance: {format_amount(uniswap_balance)}")