import xlrd, os ,xlwt
import xlutils.copy
from comm.config import DATA_PATH


def readExcel(sheet_value, row_value, col_value):
    filename = os.path.join(DATA_PATH, 'test.xls')  # file path
    date = xlrd.open_workbook(filename)  # open workbook
    sheet = date.sheet_by_index(sheet_value)  # sheet
    daterow = sheet.row(row_value)[col_value].value  # read value
    return daterow  # return value


def writeExcel(sheet_value, row_value, col_value, content):
    filename = os.path.join(DATA_PATH, 'test.xls')  # file path
    rb = xlrd.open_workbook(filename)  # open workbook
    wb = xlutils.copy.copy(rb)  # Create a new workbook using the original workbook
    ws = wb.get_sheet(sheet_value)  # get sheet 
    ws.write(row_value, col_value, content)  # write data in sheet
    wb.save(filename)  # save file


def makeExcel(row_value, col_value, name, content):
    filename = os.path.join(DATA_PATH, name)  # file path，name
    wb = xlwt.Workbook(encoding='utf-8')  # create workbook
    sheet = wb.add_sheet('sheet1')  # create sheet 
    sheet.write(row_value, col_value, content)  # write data in workbook
    wb.save(filename)  # save file
