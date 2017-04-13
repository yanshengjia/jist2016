# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 实验的第二步：单知识库生成候选实体
# 所有候选实体来自给定知识库的 labels，并没有用 BabelNet 做同义词检测。

import json
import sys
from table import *
reload(sys)
sys.setdefaultencoding("utf-8")


class Candidate(object):
    # tables: 表格数据
    # table_quantity: 表格数量
    # table_name: 表格文件的名称
    # table_path: 表格文件的路径
    # kb_name: 知识库名称
    # entity_path: 知识库实体路径
    # babelnet_path: 由 BabelNet 生成的同义词实体文件的路径
    # candidate_path: 生成好的候选实体的输出路径
    def __init__(self, table_name, table_path, kb_name, entity_path, babelnet_path, candidate_path):
        table_manager = TableManager(table_path)
        self.tables = table_manager.get_tables()  # tables[i][j][k]: 第i张表第j行第k列的单元格中的字符串
        self.table_name = table_name
        self.table_quantity = table_manager.table_quantity
        self.table_path = table_path
        self.kb_name = kb_name
        self.entity_path = entity_path
        self.babelnet_path = babelnet_path
        self.candidate_path = candidate_path

    def generate_candidate(self):
        # baidubaike
        if self.kb_name == "baidubaike":
            try:
                tables = self.tables
                baidubaike_entities = open(self.entity_path, 'r')
                baidubaike_candidate = open(self.candidate_path, 'w')
                baidubaike_entity_counter = 0
                baidubaike_entity_url = []  # [{'entity': entity, 'url': url}]
                baidubaike_entity_candidate = []    # 三维数组 baidubaike_entity_candidate[i][j][k]{'mention': m, 'candidates': [c1, c2, c3...]}

                # 读取 baidubaike 的实体及其url，存入 entity_url 字典列表
                for lines in baidubaike_entities.readlines():
                    baidubaike_entity_counter += 1
                    lines = lines.strip('\n')

                    # split
                    split = lines.split('> <')
                    entity = split[0]
                    url = split[1]

                    # clean
                    entity = entity[1:]
                    url = url[:-1]

                    # combine
                    dict = {}
                    dict['entity'] = entity
                    dict['url'] = url
                    baidubaike_entity_url.append(dict)


                # 为所有表格中的每个单元格中的 mention 生成候选实体
                # i: table number
                # j: row number
                # k: column number
                for i in range(self.table_quantity):
                    table = tables[i]
                    nRow = table.row_num
                    nCol = table.col_num
                    t = []

                    # 为第i张表格生成候选实体
                    for j in range(nRow):
                        row = []
                        for k in range(nCol):
                            dict = {}
                            candidates = []
                            cell = table.get_cell(j, k)

                            if j == 0:  # 表头不做候选实体生成
                                dict['header'] = cell
                                row.append(dict)
                                continue

                            for entity_url in baidubaike_entity_url:
                                entity = entity_url['entity']

                                if cell in entity:
                                    candidates.append(entity)

                            dict['mention'] = cell
                            dict['candidates'] = candidates
                            row.append(dict)

                        t.append(row)

                    baidubaike_entity_candidate.append(t)

            finally:
                baidubaike_entity_candidate_json = json.dumps(baidubaike_entity_candidate, ensure_ascii=False)
                baidubaike_candidate.write(baidubaike_entity_candidate_json)

                if baidubaike_entities:
                    baidubaike_entities.close()

                if baidubaike_candidate:
                    baidubaike_candidate.close()


        # hudongbaike
        if self.kb_name == "hudongbaike":
            try:
                tables = self.tables
                hudongbaike_entities = open(self.entity_path, 'r')
                hudongbaike_candidate = open(self.candidate_path, 'w')
                hudongbaike_entity_counter = 0
                hudongbaike_entity_url = []  # [{'entity': entity, 'url': url}]
                hudongbaike_entity_candidate = []    # 三维数组 hudongbaike_entity_candidate[i][j][k]{'mention': m, 'candidates': [c1, c2, c3...]}

                # 读取 hudongbaike 的实体及其url，存入 entity_url 字典列表
                for lines in hudongbaike_entities.readlines():
                    hudongbaike_entity_counter += 1
                    lines = lines.strip('\n')

                    # split
                    split = lines.split('> <')
                    entity = split[0]
                    url = split[1]

                    # clean
                    entity = entity[1:]
                    url = url[:-1]

                    # combine
                    dict = {}
                    dict['entity'] = entity
                    dict['url'] = url
                    hudongbaike_entity_url.append(dict)


                # 为所有表格中的每个单元格中的 mention 生成候选实体
                # i: table number
                # j: row number
                # k: column number
                for i in range(self.table_quantity):
                    table = tables[i]
                    nRow = table.row_num
                    nCol = table.col_num
                    t = []

                    # 为第i张表格生成候选实体
                    for j in range(nRow):
                        row = []
                        for k in range(nCol):
                            dict = {}
                            candidates = []
                            cell = table.get_cell(j, k)

                            if j == 0:  # 表头不做候选实体生成
                                dict['header'] = cell
                                row.append(dict)
                                continue

                            for entity_url in hudongbaike_entity_url:
                                entity = entity_url['entity']

                                if cell in entity:
                                    candidates.append(entity)

                            dict['mention'] = cell
                            dict['candidates'] = candidates
                            row.append(dict)

                        t.append(row)

                    hudongbaike_entity_candidate.append(t)

            finally:
                hudongbaike_entity_candidate_json = json.dumps(hudongbaike_entity_candidate, ensure_ascii=False)
                hudongbaike_candidate.write(hudongbaike_entity_candidate_json)

                if hudongbaike_entities:
                    hudongbaike_entities.close()

                if hudongbaike_candidate:
                    hudongbaike_candidate.close()


        # zhwiki
        if self.kb_name == "zhwiki":
            try:
                tables = self.tables
                zhwiki_entities = open(self.entity_path, 'r')
                zhwiki_candidate = open(self.candidate_path, 'w')
                zhwiki_entity_counter = 0
                zhwiki_entity_url = []  # [{'entity': entity, 'url': url}]
                zhwiki_entity_candidate = []    # 三维数组 zhwiki_entity_candidate[i][j][k]{'mention': m, 'candidates': [c1, c2, c3...]}

                # 读取 zhwiki 的实体及其url，存入 entity_url 字典列表
                for lines in zhwiki_entities.readlines():
                    zhwiki_entity_counter += 1
                    lines = lines.strip('\n')

                    # split
                    split = lines.split('> <')
                    entity = split[0]
                    url = split[1]

                    # clean
                    entity = entity[1:]
                    url = url[:-1]

                    # combine
                    dict = {}
                    dict['entity'] = entity
                    dict['url'] = url
                    zhwiki_entity_url.append(dict)


                # 为所有表格中的每个单元格中的 mention 生成候选实体
                # i: table number
                # j: row number
                # k: column number
                for i in range(self.table_quantity):
                    table = tables[i]
                    nRow = table.row_num
                    nCol = table.col_num
                    t = []

                    # 为第i张表格生成候选实体
                    for j in range(nRow):
                        row = []
                        for k in range(nCol):
                            dict = {}
                            candidates = []
                            cell = table.get_cell(j, k)

                            if j == 0:  # 表头不做候选实体生成
                                dict['header'] = cell
                                row.append(dict)
                                continue

                            for entity_url in zhwiki_entity_url:
                                entity = entity_url['entity']

                                if cell in entity:
                                    candidates.append(entity)

                            dict['mention'] = cell
                            dict['candidates'] = candidates
                            row.append(dict)

                        t.append(row)

                    zhwiki_entity_candidate.append(t)

            finally:
                zhwiki_entity_candidate_json = json.dumps(zhwiki_entity_candidate, ensure_ascii=False)
                zhwiki_candidate.write(zhwiki_entity_candidate_json)

                if zhwiki_entities:
                    zhwiki_entities.close()

                if zhwiki_candidate:
                    zhwiki_candidate.close()
