import ethereum
import addresses
import abis

oiler_token = ethereum.w3.eth.contract(address=addresses.oiler_token, abi=abis.oiler_token)