# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 实验的第二步：单知识库生成候选实体
# 候选实体来自给定知识库的 labels，并且使用了 BabelNet 做同义词检测。

import json
import sys
from table import *
import Levenshtein
reload(sys)
sys.setdefaultencoding("utf-8")


class Candidate(object):
    # tables: 表格数据
    # table_quantity: 表格数量
    # table_name: 表格文件的名称
    # table_path: 表格文件的路径
    # kb_name: 知识库名称
    # entity_path: 知识库实体路径，文件中包含实体以及其同义词
    # candidate_path: 生成好的候选实体的输出路径
    # threshold: 筛选候选实体与 mention 的字符串相似度阈值
    def __init__(self, table_name, table_path, kb_name, entity_path, candidate_path):
        table_manager = TableManager(table_path)
        self.tables = table_manager.get_tables()  # tables[i][j][k]: 第i张表第j行第k列的单元格中的字符串
        self.table_name = table_name
        self.table_quantity = table_manager.table_quantity
        self.table_path = table_path
        self.kb_name = kb_name
        self.entity_path = entity_path
        self.candidate_path = candidate_path
        self.threshold = 0.7

    # String Similarity
    # s1: string 1
    # s2: string 2
    def string_similarity(self, s1, s2):
        s1 = s1.decode('utf8')
        s2 = s2.decode('utf8')
        edit_distance = Levenshtein.distance(s1, s2)
        len_s1 = len(s1)
        len_s2 = len(s2)

        if len_s1 > len_s2:
            max = len_s1
        else:
            max = len_s2

        string_similarity = 1.0 - float(edit_distance) / max
        return string_similarity

    def generate_candidate(self):
        # baidubaike
        if self.kb_name == "baidubaike":
            try:
                tables = self.tables
                baidubaike_entity_file = open(self.entity_path, 'r')
                baidubaike_candidate_file = open(self.candidate_path, 'w')
                baidubaike_entity_synonym = []  # [{'entity': entity, 'synonym': [synonym list]}]
                baidubaike_entity_candidate = []    # 三维数组 baidubaike_entity_candidate[i][j][k]{'mention': m, 'candidates': [c1, c2, c3...]}

                # 读取 baidubaike 的实体及其同义词，存入 entity_synonym 字典列表
                for line in baidubaike_entity_file.readlines():
                    line = line.strip('\n')

                    # split
                    split = line.split('> <')
                    entity = split[0]
                    synonym = split[1]

                    # clean
                    entity = entity[1:]
                    synonym = synonym[:-1]

                    # combine
                    dict = {}
                    dict['entity'] = entity
                    dict['synonym'] = synonym.split(', ')
                    baidubaike_entity_synonym.append(dict)

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

                            for entity_synonym in baidubaike_entity_synonym:
                                entity = entity_synonym['entity']       # 完整的实体，包括消岐义内容 real_entity[disambiguation]
                                split = entity.split('[')
                                real_entity = split[0]              # 真实的实体，去除了消岐义内容 real_entity
                                synonym = entity_synonym['synonym']
                                flag_synonym = False

                                for syn in synonym:
                                    if cell in syn:
                                        flag_synonym = True
                                        break

                                if cell in real_entity or flag_synonym:
                                    string_similarity = self.string_similarity(cell, real_entity)

                                    if string_similarity >= self.threshold:
                                        candidates.append(entity)

                            dict['mention'] = cell
                            candidates = list(set(candidates))  # 去除重复元素
                            dict['candidates'] = candidates
                            row.append(dict)

                        t.append(row)

                    baidubaike_entity_candidate.append(t)

            finally:
                baidubaike_entity_candidate_json = json.dumps(baidubaike_entity_candidate, ensure_ascii=False)
                baidubaike_candidate_file.write(baidubaike_entity_candidate_json)

                if baidubaike_entity_file:
                    baidubaike_entity_file.close()

                if baidubaike_candidate_file:
                    baidubaike_candidate_file.close()


        # hudongbaike
        if self.kb_name == "hudongbaike":
            try:
                tables = self.tables
                hudongbaike_entity_file = open(self.entity_path, 'r')
                hudongbaike_candidate_file = open(self.candidate_path, 'w')
                hudongbaike_entity_synonym = []  # [{'entity': entity, 'synonym': [synonym list]}]
                hudongbaike_entity_candidate = []  # 三维数组 baidubaike_entity_candidate[i][j][k]{'mention': m, 'candidates': [c1, c2, c3...]}

                # 读取 hudongbaike 的实体及其同义词，存入 entity_synonym 字典列表
                for line in hudongbaike_entity_file.readlines():
                    line = line.strip('\n')

                    # split
                    split = line.split('> <')
                    entity = split[0]
                    synonym = split[1]

                    # clean
                    entity = entity[1:]
                    synonym = synonym[:-1]

                    # combine
                    dict = {}
                    dict['entity'] = entity
                    dict['synonym'] = synonym.split(', ')
                    hudongbaike_entity_synonym.append(dict)

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

                            for entity_synonym in hudongbaike_entity_synonym:
                                entity = entity_synonym['entity']  # 完整的实体，包括消岐义内容 real_entity[disambiguation]
                                split = entity.split('[')
                                real_entity = split[0]  # 真实的实体，去除了消岐义内容 real_entity
                                synonym = entity_synonym['synonym']
                                flag_synonym = False

                                for syn in synonym:
                                    if cell in syn:
                                        flag_synonym = True
                                        break

                                if cell in real_entity or flag_synonym:
                                    string_similarity = self.string_similarity(cell, real_entity)

                                    if string_similarity >= self.threshold:
                                        candidates.append(entity)

                            dict['mention'] = cell
                            candidates = list(set(candidates))  # 去除重复元素
                            dict['candidates'] = candidates
                            row.append(dict)

                        t.append(row)

                    hudongbaike_entity_candidate.append(t)

            finally:
                hudongbaike_entity_candidate_json = json.dumps(hudongbaike_entity_candidate, ensure_ascii=False)
                hudongbaike_candidate_file.write(hudongbaike_entity_candidate_json)

                if hudongbaike_entity_file:
                    hudongbaike_entity_file.close()

                if hudongbaike_candidate_file:
                    hudongbaike_candidate_file.close()

        # zhwiki
        if self.kb_name == "zhwiki":
            try:
                tables = self.tables
                zhwiki_entity_file = open(self.entity_path, 'r')
                zhwiki_candidate_file = open(self.candidate_path, 'w')
                zhwiki_entity_synonym = []  # [{'entity': entity, 'synonym': [synonym list]}]
                zhwiki_entity_candidate = []  # 三维数组 baidubaike_entity_candidate[i][j][k]{'mention': m, 'candidates': [c1, c2, c3...]}

                # 读取 zhwiki 的实体及其同义词，存入 entity_synonym 字典列表
                for line in zhwiki_entity_file.readlines():
                    line = line.strip('\n')

                    # split
                    split = line.split('> <')
                    entity = split[0]
                    synonym = split[1]

                    # clean
                    entity = entity[1:]
                    synonym = synonym[:-1]

                    # combine
                    dict = {}
                    dict['entity'] = entity
                    dict['synonym'] = synonym.split(', ')
                    zhwiki_entity_synonym.append(dict)

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

                            for entity_synonym in zhwiki_entity_synonym:
                                entity = entity_synonym['entity']  # 完整的实体，包括消岐义内容 real_entity[disambiguation]
                                split = entity.split('[')
                                real_entity = split[0]  # 真实的实体，去除了消岐义内容 real_entity
                                synonym = entity_synonym['synonym']
                                flag_synonym = False

                                for syn in synonym:
                                    if cell in syn:
                                        flag_synonym = True
                                        break

                                if cell in real_entity or flag_synonym:
                                    string_similarity = self.string_similarity(cell, real_entity)

                                    if string_similarity >= self.threshold:
                                        candidates.append(entity)

                            dict['mention'] = cell
                            candidates = list(set(candidates))  # 去除重复元素
                            dict['candidates'] = candidates
                            row.append(dict)

                        t.append(row)

                    zhwiki_entity_candidate.append(t)

            finally:
                zhwiki_entity_candidate_json = json.dumps(zhwiki_entity_candidate, ensure_ascii=False)
                zhwiki_candidate_file.write(zhwiki_entity_candidate_json)

                if zhwiki_entity_file:
                    zhwiki_entity_file.close()

                if zhwiki_candidate_file:
                    zhwiki_candidate_file.close()
