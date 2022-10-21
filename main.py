import json


types = {dict: 'OBJECT', list: 'ARRAY', bool: 'BOOLEAN', int: 'INTEGER', float: 'NUMBER', str: 'STRING', }   # noqa


class sniff_Schema:

    def __init__(self, data: dict = {}):

        self.data = data

    # Load data from json dir
    def load(self, path: str) -> dict:

        with open(path, "r") as read_data:
            self.data = json.load(read_data)['message']
        return self.data

    # sniff the schema of returned data
    def schema(self):

        def search(jsonData):

            for item in jsonData:  # go through all children items
                new_dict = {"type": types[type(jsonData[item])], "tag": "", "description": ""}
                if new_dict['type'] == "OBJECT":  # if item is object go through subitems
                    new_dict["nested-properties"] = search(jsonData[item])

                elif new_dict['type'] == "ARRAY":
                    if jsonData[item] and type(jsonData[item][0]) == dict:  #confirm list exist

                        
                        new_dict["items"] = search(jsonData[item][0])

                    #  otherwise, chage type from array to ENUM
                    else:

                        new_dict['type'] = 'ENUM'

                new_dict["required"] = False

                jsonData[item] = new_dict

            return jsonData  # backtrack returning the json

        search(self.data)

    def save(self, path):

        json_output = json.dumps(self.data, indent = 4)

        with open(path, "w") as outfile:
            outfile.write(json_output)

if __name__ == '__main__' :

    getschema = sniff_Schema()

    getschema.load('../data/data_1.json')

    getschema.schema()

    getschema.save('../schema/schema_2.json')

    getschema = sniff_Schema()

    getschema.load('../data/data_2.json')

    getschema.schema()

    getschema.save('../schema/schema_1.json')