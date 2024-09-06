"""
Desktop group module for reading JSON files and storing their values
"""
import importlib.resources
import json
import sys

import jsonschema


class Group:
    """
    A desktop group
    """
    def __init__(self, name: str, icon: str = None):
        """
        :param name: Group name
        :param icon: Group icon
        """
        self.name = name
        self.icon = icon

        self.items = []

    def add_item(self, name: str, icon: str, command: str):
        """
        Adds an item to the items list
        :param name: Item name
        :param icon: Item icon
        :param command: Item command
        """
        self.items.append(dict(name = name, icon = icon, command = command))

    def remove_item(self, name: str):
        """
        Removes an item from the items list
        :param name: Item name
        :return:
        """
        for item in self.items:
            if item['name'] == name:
                self.items.remove(item)
                break


class DGFileGroup(Group):
    """
    A desktop group created from a file
    """
    def __init__(self, dg_file: str):
        """
        :param dg_file: Location of file
        """
        # Read .desktopgroup file
        with open(dg_file, 'r', encoding="utf-8") as file:
            self.data = json.load(file)

        # Read JSON schema
        with importlib.resources.open_text('desktop-groups', 'desktopgroups.schema.json', encoding="utf-8") as schema:
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
        """
        Validates the desktopgroup file
        :return: Returns True if file is valid
        """
        try:
            jsonschema.validate(self.data, self.schema)
        except Exception as e:
            print(f'Error: {e}')
            return False
        return True
