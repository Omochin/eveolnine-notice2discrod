import os
import codecs
import json
import yaml

def main():
    def load_yaml(path):
        with codecs.open(path, 'r', 'utf-8') as file:
            data = yaml.load(file)
        return data

    items_yaml = load_yaml(os.path.join('sde', 'bsd', 'invItems.yaml'))
    names_yaml = load_yaml(os.path.join('sde', 'bsd', 'invNames.yaml'))
    moon_ids = []
    names_dict = {}
    moons_dict = {}

    for item in items_yaml:
        if item['typeID'] == 14:
            moon_ids.append(item['itemID'])

    for name in names_yaml:
        names_dict[name['itemID']] = name['itemName']

    for moon_id in moon_ids:
        moons_dict[moon_id] = names_dict[moon_id]

    with open('moons.json', 'w') as file:
        json.dump(moons_dict, file)

    types_yaml = load_yaml(os.path.join('sde', 'fsd', 'typeIDs.yaml'))
    types_dict = {}
    for i, items in types_yaml.items():
        try:
            name = items['name']['en']
        except KeyError:
            name = ''

        types_dict[i] = name.strip()

    with open('types.json', 'w') as file:
        json.dump(types_dict, file)

if __name__ == "__main__":
    main()
