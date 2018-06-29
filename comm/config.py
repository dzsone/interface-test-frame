"""
Read the configuration. The yaml used in the configuration file here can also be used as other XML, INI, etc., and the corresponding Reader needs to be added to file_reader for processing.
"""
import os
from comm.file_reader import YamlReader

# Through the absolute path of the current file, its parent directory must be the base directory of the framework, and then determine the absolute path of each layer. If your structure is different, you can modify it yourself.
# Before directly splicing the path, modify it, with the current method below, you can support different platforms such as linux and windows, it is also recommended that you use os.path.split () and os.path.join (), do not directly + '\\xxx\\ss' like this
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
CASE_PATH = os.path.join(BASE_PATH, 'testCase')

class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        """
        Yaml can be segmented by '---'. Read with YamlReader returns a list, the first item is the default section, if there are multiple sections, you can access the index to obtain.
        In this way, we can actually put the framework-related configuration in the default section, and other configuration of the project in other sections. Multiple projects can be tested in the framework.
        """
        return self.config[index].get(element)