from enum import IntEnum
import os
import json
import requests
from preston.xmlapi import Preston

class PosStates(IntEnum):
    Unanchored = 0
    Offline = 1
    Onlining = 2
    Reinforced = 3
    Online = 4

FUEL_IDS = [
    4247, # Helium Fuel Block
    4246, # Hydrogen Fuel Block
    4051, # Nitrogen Fuel Block
    4312, # Oxygen Fuel Block
]

MINIMUM_ORDER_QUANTITY = int(os.getenv('MINIMUM_ORDER_QUANTITY', 3000))

DISCORD_NOTICE_WEBHOOK_URL = os.getenv('DISCORD_NOTICE_WEBHOOK_URL', None)
DISCORD_LOG_WEBHOOK_URL = os.getenv('DISCORD_LOG_WEBHOOK_URL', None)

DISCORD_NOTICE_TEXT = os.getenv('DISCORD_NOTICE_TEXT', '{moon}: {fuel}({quantity}):thinking:')
DISCORD_LOG_TEXT = os.getenv('DISCORD_LOG_TEXT', '{moon}: {fuel}({quantity}):thinking:')

def main():
    with open('types.json', 'r') as file:
        types_dict = json.load(file)

    with open('moons.json', 'r') as file:
        moons_dict = json.load(file)

    preston = Preston(
        key=os.environ['EVEONLINE_API_KEY'],
        code=os.environ['EVEONLINE_API_CODE'],
    )

    def post(url, content):
        if url is None:
            return

        requests.post(
            url,
            data=json.dumps({'content': content}),
            headers={'content-type': 'application/json'},
        )

    rowset = preston.corp.StarbaseList()['rowset']
    if 'row' not in rowset:
        text = 'you do NOT have a pos:sob:'
        post('{moon} - {fuel}({quantity}):thinking:', text)
        post(DISCORD_LOG_WEBHOOK_URL, text)

    row = rowset['row']
    for pos in row if isinstance(row, list) else [row]:
        moon_name = moons_dict[pos['@moonID']]
        pos_state = int(pos['@state'])
        if pos_state != PosStates.Online:
            text = '"{}" is {}:scream:'.format(moon_name, PosStates(pos_state).name)
            post(DISCORD_NOTICE_WEBHOOK_URL, text)
            post(DISCORD_LOG_WEBHOOK_URL, text)

        fuels = preston.corp.StarbaseDetail(itemID=pos['@itemID'])['rowset']['row']
        for fuel in fuels:
            fuel_id = int(fuel['@typeID'])
            fuel_name = types_dict[fuel['@typeID']]
            fuel_quantity = fuel['@quantity']

            def post_fuel(url, content):
                content = content.replace('{moon}', moon_name)
                content = content.replace('{fuel}', fuel_name)
                content = content.replace('{quantity}', fuel_quantity)
                post(url, content)

            if fuel_id in FUEL_IDS:
                post_fuel(DISCORD_LOG_WEBHOOK_URL, DISCORD_LOG_TEXT)
                if int(fuel_quantity) < MINIMUM_ORDER_QUANTITY:
                    post_fuel(DISCORD_NOTICE_WEBHOOK_URL, DISCORD_NOTICE_TEXT)

if __name__ == '__main__':
    main()
