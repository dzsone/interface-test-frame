"""
File reading. YamlReader reads the yaml file.
"""
import yaml
import os
from xlrd import *


class YamlReader:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('file is not exist！')
        self._data = None

    @property
    def data(self):
        # If it is the first call to data, read the yaml document, otherwise return directly to the previously saved data
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # After load is a generator, list into a list
        return self._data



if __name__ == '__main__':
    y = './webTest/config/config.yml'
    reader = YamlReader(y)
    print(reader.data)
