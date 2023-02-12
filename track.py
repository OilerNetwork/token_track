import ethereum
import addresses
import abis
import contracts

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

