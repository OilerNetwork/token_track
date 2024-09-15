import csv
import json
import holding
from transfer import Transfer
from holding import Holding
import addresses
import address_comments
from datetime import datetime
from datetime import timedelta

with open("test-state.json", "r") as read_file:
    data = json.load(read_file)

blocks = data["blocks"]
holdings = {}
transfers = []

def print_with_indent(obj, indent=4):
    lines = str(obj).split('\n')
    indent_str = ' ' * indent
    indented = [f"{indent_str}{line}" for line in lines]
    print('\n'.join(indented))

for address, name in addresses.lookup.items():
    address = holdings.setdefault(address, Holding(address))

for address, name in address_comments.lookup.items():
    address = holdings.setdefault(address, Holding(address))
for block_number, block in blocks.items():
    for tx_hash, tx in block.items():
        for event_index, event in tx.items():
            transfer = Transfer(sender=event["from"], recipient=event["to"], value=event["value"])
            sender = transfer.sender
            recipient = transfer.recipient
            value = transfer.value
            holding_sender = holdings.setdefault(sender, Holding(sender))
            sender_before = holding_sender.balance
            holding_sender.outflows += value 
            sender_after = holding_sender.balance
            holding_recipient = holdings.setdefault(recipient, Holding(recipient))
            recipient_before = holding_recipient.balance
            holding_recipient.inflows += value
            recipient_after = holding_recipient.balance

            # Filter out transfers from specific accounts
            if '_distribution' in holding_sender.name or '_distribution' in holding_recipient.name:
                transfers.append({
                    "block": block_number,
                    "from": holding_sender.name,
                    "to": holding_recipient.name,
                    "value": value,
                    "sender_before": sender_before,
                    "sender_after": sender_after,
                    "recipient_before": recipient_before,
                    "recipient_after": recipient_after
                })

            if sender == addresses.oiler_uniswap_v2_pool:
                holding_recipient.bought += value
            if sender == addresses.lbp:
                holding_recipient.bought += value
            if sender == addresses.lbp_exchange_proxy:
                holding_recipient.bought += value

            if recipient == addresses.oiler_uniswap_v2_pool:
                holding_sender.sold += value
            if recipient == addresses.lbp:
                holding_sender.sold += value
            if recipient == addresses.lbp_exchange_proxy:
                holding_sender.sold += value

            # for each address can hold list of sources instead
            if recipient != addresses.oiler_uniswap_v2_pool:
                if holding_sender.name != 'unknown' and holding_recipient.name == 'unknown':
                    holding_recipient.name = "from_" + holding_sender.name
            # print(transfer)
            # print_with_indent(holding_sender)
            # print_with_indent(holding_recipient)
            # print()

# Sort transfers from oldest to newest
transfers.sort(key=lambda x: x['block'])

sorted_holdings = sorted(holdings.items(), key=lambda item: item[1].balance, reverse=True)
# for address, holding in sorted_holdings[:100]:
for address, holding in sorted_holdings:
    print(holding)

################## JSON dump ##########################

holding_list = [{'address': holding.address, 'name': holding.name, 'inflows': holding.inflows, 'outflows': holding.outflows, 'bought': holding.bought, 'sold': holding.sold, 'balance': holding.balance} for address, holding in sorted_holdings]

with open('sorted_holdings.json', 'w') as f:
    json.dump(holding_list, f, indent=4)

################## CSV dump ###########################

# Define the header for the CSV file
fieldnames = ['Address', 'Name', 'Inflows', 'Outflows', 'Bought', 'Sold', 'Balance']

# Open a file for writing
with open('sorted_holdings.csv', 'w', newline='') as csvfile:

    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row to the CSV file
    writer.writeheader()

    # Iterate over the sorted holdings and write each row to the CSV file
    for address, holding in sorted_holdings:
        writer.writerow({
            'Address': holding.address,
            'Name': holding.name,
            'Inflows': holding.inflows / 10**18,
            'Outflows': holding.outflows / 10**18,
            'Bought': holding.bought / 10**18,
            'Sold': holding.sold / 10**18,
            'Balance': holding.balance / 10**18,
        })

################## Transfers JSON dump ################

with open('transfers.json', 'w') as f:
    json.dump(transfers, f, indent=4)

################## Transfers CSV dump #################

# Define the header for the transfers CSV file
transfer_fieldnames = ['Date', 'From', 'To', 'Value', 'Sender_Before', 'Sender_After', 'Recipient_Before', 'Recipient_After']

# Open a file for writing
with open('transfers.csv', 'w', newline='') as csvfile:

    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=transfer_fieldnames)

    # Write the header row to the CSV file
    writer.writeheader()

    # Function to convert Ethereum block number to approximate date
    def block_to_date(block_number):
        # Known reference point: Block 12366916 occurred on May 4, 2021
        reference_block = 12366916
        reference_date = datetime(2021, 5, 4)
        # Average block time: ~13 seconds
        seconds_difference = (int(block_number) - reference_block) * 13
        estimated_date = reference_date + timedelta(seconds=seconds_difference)
        return estimated_date.strftime('%Y-%m-%d')

    # Iterate over the transfers and write each row to the CSV file
    for transfer in transfers:
        writer.writerow({
            'Date': block_to_date(transfer['block']),
            'From': transfer['from'],
            'To': transfer['to'],
            'Value': transfer['value'] / 10**18,
            'Sender_Before': transfer['sender_before'] / 10**18,
            'Sender_After': transfer['sender_after'] / 10**18,
            'Recipient_Before': transfer['recipient_before'] / 10**18,
            'Recipient_After': transfer['recipient_after'] / 10**18,
        })