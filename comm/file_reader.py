"""
File reading. YamlReader reads the yaml file and ExcelReader reads the excel.
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


class SheetTypeError(Exception):
    pass


class ExcelReader:  # please use excel_reader.py
    """
    Read the contents of the excel file. Return to list.

     Such as:
     The excel content is:
     | A | B | C |
     | A1 | B1 | C1 |
     | A2 | B2 | C2 |

     If print(ExcelReader(excel, title_line=True).data), output the result:
     [{A: A1, B: B1, C: C1}, {A:A2, B:B2, C:C2}]

     If print(ExcelReader(excel, title_line=False).data), output the result:
     [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

     You can specify sheet by index or name:
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """

    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('file is not exist！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # First row title
                for col in range(1, s.nrows):
                    # In order to traverse the remaining lines, and the first line composed dict, fight to self._data
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    # Traverse all lines and spell it in self._data
                    self._data.append(s.row_values(col))
        return self._data



if __name__ == '__main__':
    y = ' E:/test/webTest/config/config.yml'
    reader = YamlReader(y)
    print(reader.data)

    e = 'E:/test/interfaceTest/data/test.xlsx'
    reader = ExcelReader(e, title_line=True)
    print(reader.data)
