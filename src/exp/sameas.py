# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 实验的第四步：利用多知识库间sameAs关系提升链接质量

from urllib import unquote
import networkx as nx
from table import *
import json
import random


class SameAs(object):
    # table_name: 表格文件的名称
    # table_path: 表格文件的路径
    # baidubaike_edg_path: baidubaike 的实体消岐图路径
    # hudongbaike_edg_path: hudongbaike 的实体消岐图路径
    # zhwiki_edg_path: zhwiki 的实体消岐图路径
    # result_path: 最终实体链接结果的输出路径
    # baidubaike_hudongbaike_sameas_path: baidubaike 和 hudongbaike 的 sameas 数据文件路径
    # hudongbaike_zhwiki_sameas_path: hudongbaike 和 zhwiki 的 sameas 数据文件路径
    # zhwiki_baidubaike_sameas_path: zhwiki 和 baidubaike 的 sameas 数据文件路径
    def __init__(self, table_name, table_path, baidubaike_edg_path, hudongbaike_edg_path, zhwiki_edg_path, baidubaike_hudongbaike_sameas_path, hudongbaike_zhwiki_sameas_path, zhwiki_baidubaike_sameas_path, result_path):
        table_manager = TableManager(table_path)
        self.tables = table_manager.get_tables()  # 表格文件中所有表格，tables 是 Table 类型数组
        self.table_name = table_name
        self.table_path = table_path
        self.table_quantity = table_manager.table_quantity
        self.baidubaike_edg_path = baidubaike_edg_path
        self.hudongbaike_edg_path = hudongbaike_edg_path
        self.zhwiki_edg_path = zhwiki_edg_path
        self.result_path = result_path
        self.baidubaike_edg = nx.Graph()
        self.hudongbaike_edg = nx.Graph()
        self.zhwiki_edg = nx.Graph()
        self.baidubaike_hudongbaike_sameas_path = baidubaike_hudongbaike_sameas_path
        self.hudongbaike_zhwiki_sameas_path = hudongbaike_zhwiki_sameas_path
        self.zhwiki_baidubaike_sameas_path = zhwiki_baidubaike_sameas_path
        self.baidubaike_hudongbaike_sameas = []
        self.hudongbaike_zhwiki_sameas = []
        self.zhwiki_baidubaike_sameas = []
        self.kb_quantity = 3

    # 从 sameAs 文件中抽取三个知识库两两之间的 sameAs 关系
    def extract_sameAs(self):
        # input path
        baidubaike_hudongbaike_sameas_path = '../../../data/raw/sameAs/2.9_baidubaike_hudongbaike_links_zh.nt'
        hudongbaike_zhwiki_sameas_path = '../../../data/raw/sameAs/2.9_hudongbaike_zhwiki_links_zh.nt'
        zhwiki_baidubaike_sameas_path = '../../../data/raw/sameAs/2.9_zhwiki_baidubaike_links_zh.nt'

        # output path
        baidubaike_hudongbaike_sameas_output_path = '../../../data/sameas/baidubaike_hudongbaike_sameas.txt'
        hudongbaike_zhwiki_sameas_output_path = '../../../data/sameas/hudongbaike_zhwiki_sameas.txt'
        zhwiki_baidubaike_sameas_output_path = '../../../data/sameas/zhwiki_baidubaike_sameas.txt'


        # baidubaike - hudongbaike
        try:
            baidubaike_hudongbaike_sameas_ifile = open(baidubaike_hudongbaike_sameas_path, 'r')     # quantity: 1742106
            baidubaike_hudongbaike_sameas_ofile = open(baidubaike_hudongbaike_sameas_output_path, 'a')

            for line in baidubaike_hudongbaike_sameas_ifile.readlines():
                line = line.strip('\n')

                # split
                split = line.split('> <')
                baidubaike_entity = split[0]
                hudongbaike_entity = split[2]

                # clean
                baidubaike_entity = baidubaike_entity[1:]
                baidubaike_entity = baidubaike_entity.replace('http://zhishi.me/baidubaike/resource/', '')
                hudongbaike_entity = hudongbaike_entity[:-3]
                hudongbaike_entity = hudongbaike_entity.replace('http://zhishi.me/hudongbaike/resource/', '')

                # convert
                baidubaike_entity = unquote(baidubaike_entity)
                hudongbaike_entity = unquote(hudongbaike_entity)

                baidubaike_hudongbaike_link = '<' + baidubaike_entity + '> <' + hudongbaike_entity + '>\n'

                baidubaike_hudongbaike_sameas_ofile.write(baidubaike_hudongbaike_link)

        finally:
            if baidubaike_hudongbaike_sameas_ifile:
                baidubaike_hudongbaike_sameas_ifile.close()

            if baidubaike_hudongbaike_sameas_ofile:
                baidubaike_hudongbaike_sameas_ofile.close()


        # hudongbaike - zhwiki
        try:
            hudongbaikee_zhwiki_sameas_ifile = open(hudongbaike_zhwiki_sameas_path, 'r')        # quantity: 189024
            hudongbaike_zhwiki_sameas_ofile = open(hudongbaike_zhwiki_sameas_output_path, 'a')

            for line in hudongbaikee_zhwiki_sameas_ifile.readlines():
                line = line.strip('\n')

                # split
                split = line.split('> <')
                hudongbaike_entity = split[0]
                zhwiki_entity = split[2]

                # clean
                hudongbaike_entity = hudongbaike_entity[1:]
                hudongbaike_entity = hudongbaike_entity.replace('http://zhishi.me/hudongbaike/resource/', '')
                zhwiki_entity = zhwiki_entity[:-3]
                zhwiki_entity = zhwiki_entity.replace('http://zhishi.me/zhwiki/resource/', '')

                # convert
                hudongbaike_entity = unquote(hudongbaike_entity)
                zhwiki_entity = unquote(zhwiki_entity)

                hudongbaike_zhwiki_link = '<' + hudongbaike_entity + '> <' + zhwiki_entity + '>\n'

                hudongbaike_zhwiki_sameas_ofile.write(hudongbaike_zhwiki_link)

        finally:
            if hudongbaikee_zhwiki_sameas_ifile:
                hudongbaikee_zhwiki_sameas_ifile.close()

            if hudongbaike_zhwiki_sameas_ofile:
                hudongbaike_zhwiki_sameas_ofile.close()


        # zhwiki - baidubaike
        try:
            zhwiki_baidubaike_sameas_ifile = open(zhwiki_baidubaike_sameas_path, 'r')  # quantity: 206814
            zhwiki_baidubaike_sameas_ofile = open(zhwiki_baidubaike_sameas_output_path, 'a')

            for line in zhwiki_baidubaike_sameas_ifile.readlines():
                line = line.strip('\n')

                # split
                split = line.split('> <')
                zhwiki_entity = split[0]
                baidubaike_entity = split[2]

                # clean
                zhwiki_entity = zhwiki_entity[1:]
                zhwiki_entity = zhwiki_entity.replace('http://zhishi.me/zhwiki/resource/', '')
                baidubaike_entity = baidubaike_entity[:-3]
                baidubaike_entity = baidubaike_entity.replace('http://zhishi.me/baidubaike/resource/', '')

                # convert
                zhwiki_entity = unquote(zhwiki_entity)
                baidubaike_entity = unquote(baidubaike_entity)

                zhwiki_baidubaike_link = '<' + zhwiki_entity + '> <' + baidubaike_entity + '>\n'

                zhwiki_baidubaike_sameas_ofile.write(zhwiki_baidubaike_link)

        finally:
            if zhwiki_baidubaike_sameas_ifile:
                zhwiki_baidubaike_sameas_ifile.close()

            if zhwiki_baidubaike_sameas_ofile:
                zhwiki_baidubaike_sameas_ofile.close()

    # 加载实体消岐图
    # table_number: 当前表格的编号
    def load_entity_disambiguation_graph(self, table_number):
        # baidubaike
        baidubaike_edg_path = self.baidubaike_edg_path + 'edg' + str(table_number) + '.txt'
        self.baidubaike_edg = nx.read_gpickle(baidubaike_edg_path)

        # hudongbaike
        hudongbaike_edg_path = self.hudongbaike_edg_path + 'edg' + str(table_number) + '.txt'
        self.hudongbaike_edg = nx.read_gpickle(hudongbaike_edg_path)

        # zhwiki
        zhwiki_edg_path = self.zhwiki_edg_path + 'edg' + str(table_number) + '.txt'
        self.zhwiki_edg = nx.read_gpickle(zhwiki_edg_path)

    # 判断分别来自 kb1 和 kb2 的 e1 与 e2 是否存在 sameAs 关系
    def isSameAs(self, e1, kb1, e2, kb2):
        # e1 (baidubaike) - e2 (hudongbaike)
        if kb1 == 'baidubaike' and kb2 == 'hudongbaike':
            for dict in self.baidubaike_hudongbaike_sameas:
                if e1 == dict['baidubaike_entity'] and e2 == dict['hudongbaike_entity']:
                    return True

        # e1 (hudongbaike) - e2 (baidubaike)
        if kb1 == 'hudongbaike' and kb2 == 'baidubaike':
            for dict in self.baidubaike_hudongbaike_sameas:
                if e1 == dict['hudongbaike_entity'] and e2 == dict['baidubaike_entity']:
                    return True

        # e1 (hudongbaike) - e2 (zhwiki)
        if kb1 == 'hudongbaike' and kb2 == 'zhwiki':
            for dict in self.hudongbaike_zhwiki_sameas:
                if e1 == dict['hudongbaike_entity'] and e2 == dict['zhwiki_entity']:
                    return True

        # e1 (zhwiki) - e2 (hudongbaike)
        if kb1 == 'zhwiki' and kb2 == 'hudongbaike':
            for dict in self.baidubaike_hudongbaike_sameas:
                if e1 == dict['zhwiki_entity'] and e2 == dict['hudongbaike_entity']:
                    return True

        # e1 (baidubaike) - e2 (zhwiki)
        if kb1 == 'baidubaike' and kb2 == 'zhwiki':
            for dict in self.zhwiki_baidubaike_sameas:
                if e1 == dict['baidubaike_entity'] and e2 == dict['zhwiki_entity']:
                    return True

        # e1 (zhwiki) - e2 (baidubaike)
        if kb1 == 'zhwiki' and kb2 == 'baidubaike':
            for dict in self.baidubaike_hudongbaike_sameas:
                if e1 == dict['zhwiki_entity'] and e2 == dict['baidubaike_entity']:
                    return True

        return False

    def conbine_single_kb_el_result(self):
        baidubaike_result_path = '../../../data/disambiguation/baidubaike/result/'
        hudongbaike_result_path = '../../../data/disambiguation/hudongbaike/result/'
        zhwiki_result_path = '../../../data/disambiguation/zhwiki/result/'

        single_kb_el_result_path = self.result_path + 'single_kb_el_result.txt'

        try:
            single_kb_el_result_file = open(single_kb_el_result_path, 'w')
            whole = []

            for i in range(self.table_quantity):
                table = self.tables[i]
                row_num = table.row_num
                col_num = table.col_num
                t = []

                # baidubaike
                baidubaike_result_file_path = baidubaike_result_path + str(i) + '.txt'
                baidubaike_result_file = open(baidubaike_result_file_path, 'r').read()
                baidubaike_result_json = json.loads(baidubaike_result_file)

                # hudongbaike
                hudongbaike_result_file_path = hudongbaike_result_path + str(i) + '.txt'
                hudongbaike_result_file = open(hudongbaike_result_file_path, 'r').read()
                hudongbaike_result_json = json.loads(hudongbaike_result_file)

                # zhwiki
                zhwiki_result_file_path = zhwiki_result_path + str(i) + '.txt'
                zhwiki_result_file = open(zhwiki_result_file_path, 'r').read()
                zhwiki_result_json = json.loads(zhwiki_result_file)

                for r in range(row_num):
                    row = []
                    for c in range(col_num):
                        dict = {}       # {'header': h} or {'mention': m, 'entity': [(entity1, kb1), (entity2, kb2), (entity3, kb3)]}

                        if r == 0:
                            dict['header'] = baidubaike_result_json[r][c]['header']
                            row.append(dict)
                        else:
                            dict['mention'] = baidubaike_result_json[r][c]['mention']

                            entity_set = []     # [(entity1, kb1), (entity2, kb2), (entity3, kb3)]

                            # baidubaike
                            kb = 'baidubaike'
                            baidubaike_entity = baidubaike_result_json[r][c]['entity']
                            tuple = (baidubaike_entity, kb)
                            entity_set.append(tuple)

                            # hudongbaike
                            kb = 'hudongbaike'
                            hudongbaike_entity = hudongbaike_result_json[r][c]['entity']
                            tuple = (hudongbaike_entity, kb)
                            entity_set.append(tuple)

                            # zhwiki
                            kb = 'zhwiki'
                            zhwiki_entity = zhwiki_result_json[r][c]['entity']
                            tuple = (zhwiki_entity, kb)
                            entity_set.append(tuple)

                            dict['entity'] = entity_set
                            row.append(dict)
                    t.append(row)
                whole.append(t)

        finally:
            single_kb_el_result_json = json.dumps(whole, ensure_ascii=False)
            single_kb_el_result_file.write(single_kb_el_result_json)

            if single_kb_el_result_file:
                single_kb_el_result_file.close()

    # 挑选每个 mention 的候选实体概率排名列表中的前3个，来做多知识库消岐
    # 我们认为来自同一个知识库的候选实体是不存在 SameAs 关系的，因为同一个实体文件中不同实体就不存在 SameAs 关系
    def rerank(self):
        tables = self.tables
        half_number_of_kb = float(self.kb_quantity) / 2

        try:
            baidubaike_hudongbaike_sameas_file = open(self.baidubaike_hudongbaike_sameas_path, 'r')
            hudongbaike_zhwiki_sameas_file = open(self.hudongbaike_zhwiki_sameas_path, 'r')
            zhwiki_baidubaike_sameas_file = open(self.zhwiki_baidubaike_sameas_path, 'r')
            single_kb_el_result_path = self.result_path + 'single_kb_el_result.txt'
            single_kb_el_result_file = open(single_kb_el_result_path, 'r').read()
            single_kb_el_result_json = json.loads(single_kb_el_result_file)
            multiple_kb_el_result_path = self.result_path + 'multiple_kb_el_result.txt'
            multiple_kb_el_result_file = open(multiple_kb_el_result_path, 'w')

            # process baidubaike - hudongbaiek sameas data
            for line in baidubaike_hudongbaike_sameas_file.readlines():
                line = line.strip('\n')

                # split
                split = line.split('> <')
                baidubaike_entity = split[0]
                hudongbaike_entity = split[1]

                # clean
                baidubaike_entity = baidubaike_entity[1:]
                hudongbaike_entity = hudongbaike_entity[:-1]

                dict = {}
                dict['baidubaike_entity'] = baidubaike_entity
                dict['hudongbaike_entity'] = hudongbaike_entity
                self.baidubaike_hudongbaike_sameas.append(dict)

            # process hudongbaike - zhwiki sameas data
            for line in hudongbaike_zhwiki_sameas_file.readlines():
                line = line.strip('\n')

                # split
                split = line.split('> <')
                hudongbaike_entity = split[0]
                zhwiki_entity = split[1]

                # clean
                hudongbaike_entity = hudongbaike_entity[1:]
                zhwiki_entity = zhwiki_entity[:-1]

                dict = {}
                dict['hudongbaike_entity'] = hudongbaike_entity
                dict['zhwiki_entity'] = zhwiki_entity
                self.hudongbaike_zhwiki_sameas.append(dict)

            # process zhwiki - baidubaike sameas data
            for line in zhwiki_baidubaike_sameas_file.readlines():
                line = line.strip('\n')

                # split
                split = line.split('> <')
                zhwiki_entity = split[0]
                baidubaike_entity = split[1]

                # clean
                zhwiki_entity = zhwiki_entity[1:]
                baidubaike_entity = baidubaike_entity[:-1]

                dict = {}
                dict['zhwiki_entity'] = zhwiki_entity
                dict['baidubaike_entity'] = baidubaike_entity
                self.zhwiki_baidubaike_sameas.append(dict)

            whole = []

            # i: 第i张表格，从0开始
            for i in range(self.table_quantity):
                t = []
                table = tables[i]
                table_number = i
                row_num = table.row_num
                col_num = table.col_num
                mention_counter = 0

                self.load_entity_disambiguation_graph(table_number)

                baidubaike_edg = self.baidubaike_edg
                hudongbaike_edg = self.hudongbaike_edg
                zhwiki_edg = self.zhwiki_edg

                # 逐行逐列遍历表格 i 中的每个单元格
                # i: table number
                # r: row number
                # c: column number
                for r in range(row_num):
                    row = []

                    for c in range(col_num):
                        cell = {}   # {'header': h} or {'mention': m, 'entity': [(entity1, kb1), (entity2, kb2), (entity3, kb3)]}
                        mention = table.get_cell(r, c)  # unicode

                        if r == 0:  # 表头不做实体链接
                            cell['header'] = mention
                            row.append(cell)
                        else:
                            cell['mention'] = mention

                            baidubaike_ranking_list = []    # [(entity1, kb1, rank), (entity2, kb1, rank), (entity3, kb1, rank)]
                            hudongbaike_ranking_list = []
                            zhwiki_ranking_list = []

                            # get baidubaike ranking list
                            kb = 'baidubaike'
                            ranking = baidubaike_edg.node[mention_counter]['ranking']   # [(entity1_number, probability1), (entity2_number, probability2)]
                            rank = 1

                            if baidubaike_edg.node[mention_counter]['NIL'] == False:
                                if len(ranking) < 3:
                                    for tuple in ranking:
                                        entity_number = tuple[0]
                                        entity = baidubaike_edg.node[entity_number]['candidate']
                                        entity_kb_tuple = (entity, kb, rank)
                                        baidubaike_ranking_list.append(entity_kb_tuple)
                                        rank += 1
                                else:
                                    for p in range(3):
                                        entity_number = ranking[p][0]
                                        entity = baidubaike_edg.node[entity_number]['candidate']
                                        entity_kb_tuple = (entity, kb, rank)
                                        baidubaike_ranking_list.append(entity_kb_tuple)
                                        rank += 1


                            # get hudongbaike ranking list
                            kb = 'hudongbaike'
                            ranking = hudongbaike_edg.node[mention_counter]['ranking']  # [(entity1_number, probability1), (entity2_number, probability2)]
                            rank = 1

                            if hudongbaike_edg.node[mention_counter]['NIL'] == False:
                                if len(ranking) < 3:
                                    for tuple in ranking:
                                        entity_number = tuple[0]
                                        entity = hudongbaike_edg.node[entity_number]['candidate']
                                        entity_kb_tuple = (entity, kb, rank)
                                        hudongbaike_ranking_list.append(entity_kb_tuple)
                                        rank += 1
                                else:
                                    for p in range(3):
                                        entity_number = ranking[p][0]
                                        entity = hudongbaike_edg.node[entity_number]['candidate']
                                        entity_kb_tuple = (entity, kb, rank)
                                        hudongbaike_ranking_list.append(entity_kb_tuple)
                                        rank += 1


                            # get zhwiki ranking list
                            kb = 'zhwiki'
                            ranking = zhwiki_edg.node[mention_counter]['ranking']  # [(entity1_number, probability1), (entity2_number, probability2)]
                            rank = 1

                            if zhwiki_edg.node[mention_counter]['NIL'] == False:
                                if len(ranking) < 3:
                                    for tuple in ranking:
                                        entity_number = tuple[0]
                                        entity = zhwiki_edg.node[entity_number]['candidate']
                                        entity_kb_tuple = (entity, kb, rank)
                                        zhwiki_ranking_list.append(entity_kb_tuple)
                                        rank += 1
                                else:
                                    for p in range(3):
                                        entity_number = ranking[p][0]
                                        entity = zhwiki_edg.node[entity_number]['candidate']
                                        entity_kb_tuple = (entity, kb, rank)
                                        zhwiki_ranking_list.append(entity_kb_tuple)
                                        rank += 1

                            mention_counter += 1

                            list = []   # [{'set': [(entity1, kb1, rank), (entity2, kb2, rank)], 'average_ranking': 1.25, 'average_ranking_rank': 1, 'highest_ranking': 1, 'highest_ranking_rank': 1, 'set_size': size of the set, 'flag_less': True}]

                            # baidubaike - hudongbaike - zhwiki
                            for baidubaike_candidate_index in range(len(baidubaike_ranking_list)):
                                set = []    # [(entity1, kb1, rank), (entity2, kb2, rank)]
                                baidubaike_entity = baidubaike_ranking_list[baidubaike_candidate_index][0]
                                set.append(baidubaike_ranking_list[baidubaike_candidate_index])
                                flag_hudongbaike_pop = False

                                for hudongbaike_candidate_index in range(len(hudongbaike_ranking_list)):
                                    hudongbaike_entity = hudongbaike_ranking_list[hudongbaike_candidate_index][0]

                                    if self.isSameAs(baidubaike_entity, 'baidubaike', hudongbaike_entity, 'hudongbaike'):
                                        set.append(hudongbaike_ranking_list[hudongbaike_candidate_index])
                                        hudongbaike_pop_index = hudongbaike_candidate_index
                                        flag_hudongbaike_pop = True
                                        flag_zhwiki_pop = False

                                        for zhwiki_candidate_index in range(len(zhwiki_ranking_list)):
                                            zhwiki_entity = zhwiki_ranking_list[zhwiki_candidate_index][0]

                                            if self.isSameAs(hudongbaike_entity, 'hudongbaike', zhwiki_entity, 'zhwiki'):
                                                set.append(zhwiki_ranking_list[zhwiki_candidate_index])
                                                zhwiki_pop_index = zhwiki_candidate_index
                                                flag_zhwiki_pop = True
                                                break

                                        if flag_zhwiki_pop:
                                            zhwiki_ranking_list.pop(zhwiki_pop_index)

                                        break

                                if flag_hudongbaike_pop:
                                    hudongbaike_ranking_list.pop(hudongbaike_pop_index)

                                flag_zhwiki_pop = False
                                for zhwiki_candidate_index in range(len(zhwiki_ranking_list)):
                                    zhwiki_entity = zhwiki_ranking_list[zhwiki_candidate_index][0]

                                    if self.isSameAs(baidubaike_entity, 'baidubaike', zhwiki_entity, 'zhwiki'):
                                        set.append(zhwiki_ranking_list[zhwiki_candidate_index])
                                        zhwiki_pop_index = zhwiki_candidate_index
                                        flag_zhwiki_pop = True
                                        break

                                if flag_zhwiki_pop:
                                    zhwiki_ranking_list.pop(zhwiki_pop_index)

                                # build dict
                                dict = {}  # {'set': [(entity1, kb1, rank), (entity2, kb2, rank)], 'average_ranking': 1.25, 'average_ranking_rank': 1, 'highest_ranking': 1, 'highest_ranking_rank': 1, 'set_size': size of the set, 'flag_less': True}
                                set_size = len(set)
                                dict['set_size'] = set_size
                                dict['set'] = set

                                if set_size < half_number_of_kb:
                                    dict['flag_less'] = True
                                else:
                                    dict['flag_less'] = False

                                average_ranking = 0
                                highest_ranking = 3

                                for candidate in set:
                                    rank = candidate[2]

                                    if rank < highest_ranking:
                                        highest_ranking = rank

                                    average_ranking += rank

                                average_ranking /= float(set_size)
                                dict['average_ranking'] = average_ranking
                                dict['highest_ranking'] = highest_ranking
                                dict['average_ranking_rank'] = 1
                                dict['highest_ranking_rank'] = 1
                                list.append(dict)

                            # hudongbaike - zhwiki
                            for hudongbaike_candidate_index in range(len(hudongbaike_ranking_list)):
                                set = []        # [(entity1, kb1, rank), (entity2, kb2, rank)]
                                hudongbaike_entity = hudongbaike_ranking_list[hudongbaike_candidate_index][0]
                                set.append(hudongbaike_ranking_list[hudongbaike_candidate_index])
                                flag_zhwiki_pop = False

                                for zhwiki_candidate_index in range(len(zhwiki_ranking_list)):
                                    zhwiki_entity = zhwiki_ranking_list[zhwiki_candidate_index][0]

                                    if self.isSameAs(hudongbaike_entity, 'hudongbaike', zhwiki_entity, 'zhwiki'):
                                        set.append(zhwiki_ranking_list[zhwiki_candidate_index])
                                        zhwiki_pop_index = zhwiki_candidate_index
                                        flag_zhwiki_pop = True
                                        break

                                if flag_zhwiki_pop:
                                    zhwiki_ranking_list.pop(zhwiki_pop_index)

                                # build dict
                                dict = {}
                                set_size = len(set)
                                dict['set_size'] = set_size
                                dict['set'] = set

                                if set_size < half_number_of_kb:
                                    dict['flag_less'] = True
                                else:
                                    dict['flag_less'] = False

                                average_ranking = 0
                                highest_ranking = 3

                                for candidate in set:
                                    rank = candidate[2]

                                    if rank < highest_ranking:
                                        highest_ranking = rank

                                    average_ranking += rank

                                average_ranking /= float(set_size)
                                dict['average_ranking'] = average_ranking
                                dict['highest_ranking'] = highest_ranking
                                dict['average_ranking_rank'] = 1
                                dict['highest_ranking_rank'] = 1
                                list.append(dict)

                            # zhwiki
                            for zhwiki_candidate_index in range(len(zhwiki_ranking_list)):
                                set = []        # [(entity1, kb1, rank), (entity2, kb2, rank)]
                                set.append(zhwiki_ranking_list[zhwiki_candidate_index])

                                # build dict
                                dict = {}
                                set_size = len(set)
                                dict['set_size'] = set_size
                                dict['set'] = set

                                if set_size < half_number_of_kb:
                                    dict['flag_less'] = True
                                else:
                                    dict['flag_less'] = False

                                average_ranking = 0
                                highest_ranking = 3

                                for candidate in set:
                                    rank = candidate[2]

                                    if rank < highest_ranking:
                                        highest_ranking = rank

                                    average_ranking += rank

                                average_ranking /= float(set_size)
                                dict['average_ranking'] = average_ranking
                                dict['highest_ranking'] = highest_ranking
                                dict['average_ranking_rank'] = 1
                                dict['highest_ranking_rank'] = 1
                                list.append(dict)

                            # rank the average_ranking
                            list.sort(key=lambda x: x['average_ranking'])  # 按照 average_ranking 顺序排序，下标越大 average_ranking 越大
                            current_rank = 1

                            for index in range(len(list)):
                                if index == 0:
                                    list[index]['average_ranking_rank'] = current_rank
                                else:
                                    if list[index]['average_ranking'] > list[index-1]['average_ranking']:
                                        current_rank += 1
                                        list[index]['average_ranking_rank'] = current_rank
                                    else:
                                        list[index]['average_ranking_rank'] = current_rank

                            # rank the highest_ranking
                            list.sort(key=lambda x: x['highest_ranking'])  # 按照 highest_ranking 顺序排序，下标越大 highest_ranking 越大
                            current_rank = 1

                            for index in range(len(list)):
                                if index == 0:
                                    list[index]['highest_ranking_rank'] = current_rank
                                else:
                                    if list[index]['highest_ranking'] > list[index - 1]['highest_ranking']:
                                        current_rank += 1
                                        list[index]['highest_ranking_rank'] = current_rank
                                    else:
                                        list[index]['highest_ranking_rank'] = current_rank

                            # Rule 3
                            flag_less = True

                            for d in list:
                                if d['flag_less'] == False:
                                    flag_less = False
                                    break

                            if flag_less:
                                cell['entity'] = single_kb_el_result_json[i][r][c]['entity']
                                row.append(cell)
                                continue

                            # Rule 1 & Rule 2
                            final_candidate_set_list = []   # [[(entity1, kb1), (entity2, kb2)], [(entity3, kb3)]]

                            for d in list:
                                if d['average_ranking_rank'] == 1 and d['highest_ranking_rank'] == 1 and d['flag_less'] == False:
                                    set = d['set']
                                    entity_kb_set = []      # [(entity1, kb1), (entity2, kb2)]

                                    for triple in set:
                                        entity = triple[0]
                                        kb = triple[1]
                                        tuple = (entity, kb)
                                        entity_kb_set.append(tuple)

                                    final_candidate_set_list.append(entity_kb_set)

                            if len(final_candidate_set_list) == 0:
                                cell['entity'] = single_kb_el_result_json[i][r][c]['entity']
                                row.append(cell)
                            elif len(final_candidate_set_list) == 1:
                                cell['entity'] = final_candidate_set_list[0]
                                row.append(cell)
                            else:
                                cell['entity'] = final_candidate_set_list[random.randint(0, len(final_candidate_set_list) - 1)]
                                row.append(cell)
                    t.append(row)
                whole.append(t)

        finally:
            multiple_kb_el_result_json = json.dumps(whole, ensure_ascii=False)
            multiple_kb_el_result_file.write(multiple_kb_el_result_json)

            if baidubaike_hudongbaike_sameas_file:
                baidubaike_hudongbaike_sameas_file.close()

            if hudongbaike_zhwiki_sameas_file:
                hudongbaike_zhwiki_sameas_file.close()

            if zhwiki_baidubaike_sameas_file:
                zhwiki_baidubaike_sameas_file.close()

            if multiple_kb_el_result_file:
                multiple_kb_el_result_file.close()
