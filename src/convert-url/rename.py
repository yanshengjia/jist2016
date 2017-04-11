# !/usr/bin/python
# coding=utf8
# Created by sjyan @2017-03-19
# 修改3个知识库人工标注结果的id，原始文件来自 https://github.com/jxls080511/MK-EL


from urllib import quote
import json
import sys
import xlrd
reload(sys)
sys.setdefaultencoding("utf-8")


class Table:
    def __init__(self, table, row_num, col_num):
        self.table = table
        self.row_num = row_num
        self.col_num = col_num
    def __getitem__(self, i):
        return self.table[i]

    def getMentionContext(self, r, c):
        res = []
        for i in range(self.row_num):
            if i == r:
                continue
            res.append(self.table[i][c])

        for j in range(self.col_num):
            if j == c:
                continue
            res.append(self.table[r][j])
        return res


# 获取 excel 文件中的所有表格
class tableManager:
    def __init__(self):
        self.excel = xlrd.open_workbook("../../../data/mkel/table/table_123.xls")

    def getTable(self):
        table = self.excel.sheet_by_name('Sheet1')
        tables = []     # tables.xls 中的所有表格，数组元素类型为 Table

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

            t = []
            for rr in range(r, next_r):
                row = []
                for cc in range(0,next_c):
                    row.append(table.cell(rr,cc).value)
                t.append(row)
            tables.append(Table(t, next_r - r, next_c))
            if down_flag:
                break
            else:
                r = next_r + 1

        return tables


# 主函数
if __name__ == '__main__':
    tablemaster = tableManager()
    tables = tablemaster.getTable()

    list = open('./id_list.txt', 'r') # list0: baidubaike, list1: hudongbaike, list2: zhwiki
    list_counter = 0

    # 修改三个知识库的人工标注结果文件
    for route in list.readlines():
        route = route.strip('\n')
        infile = open(route, 'r').read()

        tables_json = json.loads(infile, encoding='utf8')

        # i: table number
        # j: row number
        # k: column number
        for i in range(0, len(tables_json)):
            for j in range(0, len(tables_json[i])):
                for k in range(0, len(tables_json[i][j])):
                    if j == 0:  # 表头 不做EL
                        tables_json[i][j][k]['head'] = tables[i][j][k]
                        if tables_json[i][j][k].has_key('name'):
                            tables_json[i][j][k].pop('name')
                            tables_json[i][j][k].pop('id')
                    else:
                        tables_json[i][j][k]['mention'] = tables[i][j][k]
                        if tables_json[i][j][k].has_key('name'):
                            tables_json[i][j][k]['entity'] = tables_json[i][j][k].pop('name')
                            entity = tables_json[i][j][k]["entity"]
                            entity = entity.replace("["," (")
                            entity = entity.replace("]",")")
                            tables_json[i][j][k]["entity"] = entity
                            tables_json[i][j][k].pop('id')
                        else:
                            tables_json[i][j][k]['entity'] = 'Null'

        tables_str = json.dumps(tables_json, ensure_ascii=False)

        if list_counter == 0:
            outfile = open("../../../data/mkel/baidubaike/human_mark_baidubaike_entity.txt", "w")
            outfile.write(tables_str)
        if list_counter == 1:
            outfile = open("../../../data/mkel/hudongbaike/human_mark_hudongbaike_entity.txt", "w")
            outfile.write(tables_str)
        if list_counter == 2:
            outfile = open("../../../data/mkel/zhwiki/human_mark_zhwiki_entity.txt", "w")
            outfile.write(tables_str)

        list_counter += 1

        outfile.close()








