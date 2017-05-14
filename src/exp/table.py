# !/usr/bin/python
# -*- coding:utf-8 -*-  
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 表格类与读取表格文件的类

import xlrd
import jieba

class Table(object):
    # table: 二维数组存储表格中的内容
    # row_num: 表格的行数
    # col_num: 表格的列数
    def __init__(self, table, row_num, col_num):
        self.table = table
        self.row_num = row_num
        self.col_num = col_num
        self.mention_quantity = (row_num - 1) * col_num

    # 获取表格中位于 (i, j) 处的单元格值 (unicode)
    def get_cell(self, i, j):
        return self.table[i][j]

    # 获取表格中 mention 的数量
    # 一开始认为表格中所有单元格中的字符串都是 mention，如果有链接不到实体的 mention，之后给它打一个标签 NIL 表示 "无法链接"
    def get_mention_quantity(self):
        mention_quantity = (self.row_num - 1) * self.col_num
        return mention_quantity

    # 获取表格中位于 (r, c) 处的单元格的同行同列的所有单元格值
    def get_mention_context(self, r, c):
        mention_context = []

        for i in range(self.row_num):
            if i == r:
                continue
            mention_context.append(self.get_cell(i, c))  # unicode

        for j in range(self.col_num):
            if j == c:
                continue
            mention_context.append(self.get_cell(r, j))  # unicode

        return mention_context


# 获取 excel 文件中的所有表格
class TableManager(object):
    def __init__(self, table_path):
        self.table_path = table_path
        self.excel = xlrd.open_workbook(self.table_path)
        self.table_quantity = 0

    # 读取 xls 文件中的所有表格，每个表格都是 Table 类型
    def get_tables(self):
        table = self.excel.sheet_by_name('Sheet1')
        tables = []     # tables.xls 中的所有表格，数组元素类型为 Table
        counter = 0

        nrows = table.nrows
        ncols = table.ncols

        # 按列存储
        r = 0
        down_flag = False
        while True:
            r += 1

            # 获取当前表格的行数
            next_r = r
            while True:
                if next_r == nrows:
                    down_flag = True
                    break
                if table.cell(next_r, 0).value != '':
                    next_r += 1
                else:
                    break

            # 获取当前表格的列数
            next_c = 0
            while True:
                if next_c == ncols:
                    break
                if table.cell(r, next_c).value != '':
                    next_c += 1
                else:
                    break

            t = []  # 每张表格
            for rr in range(r, next_r):
                row = []
                for cc in range(0, next_c):
                    row.append(table.cell(rr, cc).value)
                t.append(row)

            tables.append(Table(t, next_r - r, next_c))
            counter += 1

            if down_flag:
                break
            else:
                r = next_r + 1

        self.table_quantity = counter

        return tables