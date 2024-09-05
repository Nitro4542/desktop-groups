import json
import sys

import jsonschema

class Group:
    def __init__(self, name, icon = None):
        self.name = name
        self.icon = icon

        self.items = []

    def add_item(self, name, icon, command):
        self.items.append(dict(name = name, icon = icon, command = command))

    def remove_item(self, name):
        for item in self.items:
            if item['name'] == name:
                self.items.remove(item)
                break


class DGFileGroup(Group):
    def __init__(self, dg_file):
        # Read .desktopgroup file
        with open(dg_file, 'r') as file:
            self.data = json.load(file)

        # Read JSON schema
        with open('desktopgroups.schema.json', 'r') as schema:
            self.schema = json.load(schema)

        # Validate JSON
        if not self.validate():
            print('Error while validating JSON')
            sys.exit(1)

        # Initialize Group class
        super().__init__(self.data.get('group', {}).get('name'), self.data.get('group', {}).get('icon'))

        # Add items to self.items list
        group = self.data.get('group', {})
        items = group.get('items', [])

        for item in items:
            self.items.append(item)

    def validate(self):
        try:
            jsonschema.validate(self.data, self.schema)
        except jsonschema.exceptions as e:
            print(f'Error: {e}')
            return False
        return True
