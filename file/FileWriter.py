import os
import json

JSON_EXTENSION = '.json'
NO_CONTENT = 'No content to be written.'

class FileWriter:

    __path__ = ''
    __field__ = ''

    def __init__(self, path, field='name'):
        self.__field__ = field
        self.__path__ = path

    def write_json(self, content):
        """Write the content passed in a JSON file""""
        if not content:
            raise Exception(NO_CONTENT)

        json_dict = json.loads(content)
        json_file = open(self.__path__ + json_dict[self.__field__] + JSON_EXTENSION, 'w')
        json_file.write(content)
        json_file.close()
        json_file = open(self.__path__ + json_dict[self.__field__] + JSON_EXTENSION, 'r')
        