import json
import os
import requests
from preston.xmlapi import Preston

FUEL_IDS = [
    4246
]

def main():
    with open('types.json', 'r') as file:
        types_dict = json.load(file)

    preston = Preston(
        key=os.environ['EVEONLINE_API_KEY_ID'],
        code=os.environ['EVEONLINE_API_VCODE'],
    )

    def post(url, content):
        requests.post(
            url,
            data=json.dumps({'content': content}),
            headers={'content-type': 'application/json'},
        )

    pos = preston.corp.StarbaseList()['rowset']
    if pos['@name'] == 'starbases':
        pos_id = preston.corp.StarbaseList()['rowset']['row']['@itemID']
        fuels = preston.corp.StarbaseDetail(itemID=pos_id)['rowset']['row']
        for fuel in fuels:
            type_id = int(fuel['@typeID'])
            name = types_dict[fuel['@typeID']]
            quantity = int(fuel['@quantity'])

            if type_id in FUEL_IDS:
                if 'DISCORD_TEST_WEBHOOK_URL' in os.environ:
                    post(
                        os.environ['DISCORD_TEST_WEBHOOK_URL'],
                        "{}({})".format(name, quantity),
                    )
                if quantity < int(os.getenv('MINIMUM_ORDER_QUANTITY', 2800)):
                    post(
                        os.environ['DISCORD_WEBHOOK_URL'],
                        "@everyone {}({}):scream:".format(name, quantity),
                    )

if __name__ == '__main__':
    main()
