import codecs
import json
import yaml

def main():
    with codecs.open('typeIDs.yaml', 'r', 'utf-8') as file:
        types_yaml = yaml.load(file)

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
