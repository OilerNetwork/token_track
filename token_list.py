import csv
import json
import holding
from transfer import Transfer
from holding import Holding
import addresses

with open("test-state.json", "r") as read_file:
    data = json.load(read_file)

blocks = data["blocks"]
holdings = {}

def print_with_indent(obj, indent=4):
    lines = str(obj).split('\n')
    indent_str = ' ' * indent
    indented = [f"{indent_str}{line}" for line in lines]
    print('\n'.join(indented))

for block_number, block in blocks.items():
    for tx_hash, tx in block.items():
        for event_index, event in tx.items():
            transfer = Transfer(sender=event["from"], recipient=event["to"], value=event["value"])
            sender = transfer.sender
            recipient = transfer.recipient
            value = transfer.value
            holding_sender = holdings.setdefault(sender, Holding(sender))
            holding_sender.outflows += value 
            holding_recipient = holdings.setdefault(recipient, Holding(recipient))
            holding_recipient.inflows += value
            if recipient == addresses.oiler_uniswap_v2_pool:
                holding_sender.sold += value
            # print(transfer)
            # print_with_indent(holding_sender)
            # print_with_indent(holding_recipient)
            # print()

sorted_holdings = sorted(holdings.items(), key=lambda item: item[1].balance, reverse=True)
for address, holding in sorted_holdings[:100]:
    print(holding)

################## JSON dump ##########################

holding_list = [{'address': holding.address, 'name': holding.name, 'inflows': holding.inflows, 'outflows': holding.outflows, 'sold': holding.sold, 'balance': holding.balance} for address, holding in sorted_holdings]

with open('sorted_holdings.json', 'w') as f:
    json.dump(holding_list, f, indent=4)

################## CSV dump ###########################

# Define the header for the CSV file
fieldnames = ['Address', 'Name', 'Inflows', 'Outflows', 'Sold', 'Balance']

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
            'Inflows': holding.inflows,
            'Outflows': holding.outflows,
            'Sold': holding.sold,
            'Balance': holding.balance,
        })