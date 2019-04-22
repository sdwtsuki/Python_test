import re
import xlrd
import xlwt
from xlutils.copy import copy
import pandas as pd

def write_excel():
    excel_path = r'D:\Downloads\备份策略20190301.xlsx'
    save_path = r'D:\Downloads\备份策略20190301_233.xls'
    sheet_name = '数仓'
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_name(sheet_name)
    rows = sheet.nrows  # excel文件的行数
    cols = sheet.ncols  # ecel文件的列数

    book2 = copy(book)  # 拷贝一份原来的excel
    sheet2 = book2.get_sheet(sheet_name)  # 获取sheet页，book2现在的是xlutils里的方法，不是xlrd的
    col_hostname = 0

    for ii in range(0, sheet.ncols):  # tabvInfo取到需要取的列的excel列号
        if sheet.cell(0, ii).value == 'Host Information':
            col_hostname = ii

    print(rows)
    for rownum in range(1, rows):  # 读取行
        celldata = sheet.cell(rownum, col_hostname).value  # 读取单元格数据



    print('程序执行完毕')

write_excel()
