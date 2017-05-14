# !/usr/bin/python
# -*- coding:utf-8 -*-  
# Author: Shengjia Yan
# Date: 2017/5/10
# Email: sjyan@seu.edu.cn

# 人工标注

import json
from table import *

class Mark(object):
    # table_path: 表格路径
    # baidubaike_candidates_path: baidubaike 候选实体路径
    # hudongbaike_candidates_path: hudongbaike 候选实体路径
    # zhwiki_candidates_path: zhwiki 候选实体路径
    # baidubaike_single_human_mark_path: 基于 baidubaike 的分表格EL人工标注结果路径
    # hudongbaike_single_human_mark_path: 基于 hudongbaike 的分表格EL人工标注结果路径
    # zhwiki_single_human_mark_path: 基于 zhwiki 的分表格EL人工标注结果路径
    # baidubaike_total_human_mark_path:  基于 baidubaike 的整个表格文件EL人工标注结果路径
    # hudongbaike_total_human_mark_path: 基于 hudongbaike 的整个表格文件EL人工标注结果路径
    # zhwiki_total_human_mark_path:  基于 zhwiki 的整个表格文件EL人工标注结果路径
    def __init__(self, table_path, baidubaike_candidates_path, hudongbaike_candidates_path, zhwiki_candidates_path, baidubaike_single_human_mark_path, hudongbaike_single_human_mark_path, zhwiki_single_human_mark_path, baidubaike_total_human_mark_path, hudongbaike_total_human_mark_path, zhwiki_total_human_mark_path):
        self.table_path = table_path
        table_manager = TableManager(table_path)
        self.tables = table_manager.get_tables()
        self.table_quantity = table_manager.table_quantity
        self.baidubaike_candidates_path = baidubaike_candidates_path
        self.hudongbaike_candidates_path = hudongbaike_candidates_path
        self.zhwiki_candidates_path = zhwiki_candidates_path
        self.baidubaike_single_human_mark_path = baidubaike_single_human_mark_path
        self.hudongbaike_single_human_mark_path = hudongbaike_single_human_mark_path
        self.zhwiki_single_human_mark_path = zhwiki_single_human_mark_path
        self.baidubaike_total_human_mark_path = baidubaike_total_human_mark_path
        self.hudongbaike_total_human_mark_path = hudongbaike_total_human_mark_path
        self.zhwiki_total_human_mark_path = zhwiki_total_human_mark_path

    def mark(self):
        try:
            baidubaike_candidates_file = open(self.baidubaike_candidates_path, 'r')
            baidubaike_candidates = baidubaike_candidates_file.read()
            baidubaike_candidates_json = json.loads(baidubaike_candidates, encoding='utf8')

            hudongbaike_candidates_file = open(self.hudongbaike_candidates_path, 'r')
            hudongbaike_candidates = hudongbaike_candidates_file.read()
            hudongbaike_candidates_json = json.loads(hudongbaike_candidates, encoding='utf8')

            zhwiki_candidates_file = open(self.zhwiki_candidates_path, 'r')
            zhwiki_candidates = zhwiki_candidates_file.read()
            zhwiki_candidates_json = json.loads(zhwiki_candidates, encoding='utf8')


            # for i in range(self.table_quantity):
            for i in range(28, 123):
                table = self.tables[i]
                row_num = table.row_num
                col_num = table.col_num
                t_baidubaike = []
                t_hudongbaike = []
                t_zhwiki = []

                try:
                    baidubaike_single_human_mark_path = self.baidubaike_single_human_mark_path + str(i) + '.txt'
                    baidubaike_single_human_mark_file = open(baidubaike_single_human_mark_path, 'w')
                    hudongbaike_single_human_mark_path = self.hudongbaike_single_human_mark_path + str(i) + '.txt'
                    hudongbaike_single_human_mark_file = open(hudongbaike_single_human_mark_path, 'w')
                    zhwiki_single_human_mark_path = self.zhwiki_single_human_mark_path + str(i) + '.txt'
                    zhwiki_single_human_mark_file = open(zhwiki_single_human_mark_path, 'w')

                    for r in range(row_num):
                        row_baidubaike = []
                        row_hudongbaike = []
                        row_zhwiki = []

                        for c in range(col_num):
                            dict_baidubaike = {}
                            dict_hudongbaike = {}
                            dict_zhwiki = {}

                            if r == 0:
                                dict_baidubaike['header'] = baidubaike_candidates_json[i][r][c]['header']
                                row_baidubaike.append(dict_baidubaike)
                                dict_hudongbaike['header'] = hudongbaike_candidates_json[i][r][c]['header']
                                row_hudongbaike.append(dict_hudongbaike)
                                dict_zhwiki['header'] = zhwiki_candidates_json[i][r][c]['header']
                                row_zhwiki.append(dict_zhwiki)
                                continue

                            mention = baidubaike_candidates_json[i][r][c]['mention']
                            dict_baidubaike['mention'] = mention
                            dict_hudongbaike['mention'] = mention
                            dict_zhwiki['mention'] = mention

                            print '---------------------------------------------------------'
                            print 'Table ' + str(i) + ' Row ' + str(r) + ' Column ' + str(c)
                            print 'Mention: ' + mention

                            ############################
                            print 'Result: '
                            result_list = multiple_kb_el_result_json[i][r][c]['entity']
                            result_str = ''

                            for p in range(len(result_list)):
                                result_str += result_list[p][0]
                                result_str += '<'
                                result_str += result_list[p][1]
                                result_str += '> '

                            print result_str
                            print
                            ###########################

                            # baidubaike
                            print 'Baidubaike Candidates List:'
                            baidubaike_candidates_list = baidubaike_candidates_json[i][r][c]['candidates']
                            baidubaike_candidates_str = ''

                            if len(baidubaike_candidates_list) == 0:
                                baidubaike_entity = 'Null'
                                print 'Null'
                                print
                            elif len(baidubaike_candidates_list) == 1:
                                baidubaike_entity = baidubaike_candidates_json[i][r][c]['candidates'][0]
                                print 'Only 1 candidate <' + baidubaike_entity + '>. Auto selection.'
                                print
                            else:
                                for k in range(len(baidubaike_candidates_list)):
                                    baidubaike_candidates_str += str(k)
                                    baidubaike_candidates_str += '. '
                                    baidubaike_candidates_str += baidubaike_candidates_list[k]
                                    baidubaike_candidates_str += '\n'

                                print baidubaike_candidates_str
                                candidate_index = input('Input the number before the entity you choose(If there is no referent entity, just input -1): ')
                                print

                                if int(candidate_index) == -1:
                                    baidubaike_entity = 'Null'
                                else:
                                    baidubaike_entity = baidubaike_candidates_json[i][r][c]['candidates'][int(candidate_index)]


                            # hudongbaike
                            print 'Hudongbaike Candidates List:'
                            hudongbaike_candidates_list = hudongbaike_candidates_json[i][r][c]['candidates']
                            hudongbaike_candidates_str = ''

                            if len(hudongbaike_candidates_list) == 0:
                                hudongbaike_entity = 'Null'
                                print 'Null'
                                print
                            elif len(hudongbaike_candidates_list) == 1:
                                hudongbaike_entity = hudongbaike_candidates_json[i][r][c]['candidates'][0]
                                print 'Only 1 candidate <' + hudongbaike_entity + '>. Auto selection.'
                                print
                            else:
                                for k in range(len(hudongbaike_candidates_list)):
                                    hudongbaike_candidates_str += str(k)
                                    hudongbaike_candidates_str += '. '
                                    hudongbaike_candidates_str += hudongbaike_candidates_list[k]
                                    hudongbaike_candidates_str += '\n'

                                print hudongbaike_candidates_str
                                candidate_index = input('Input the number before the entity you choose(If there is no referent entity, just input -1): ')
                                print

                                if int(candidate_index) == -1:
                                    hudongbaike_entity = 'Null'
                                else:
                                    hudongbaike_entity = hudongbaike_candidates_json[i][r][c]['candidates'][int(candidate_index)]


                            # zhwiki
                            print 'Zhwiki Candidates List:'
                            zhwiki_candidates_list = zhwiki_candidates_json[i][r][c]['candidates']
                            zhwiki_candidates_str = ''

                            if len(zhwiki_candidates_list) == 0:
                                zhwiki_entity = 'Null'
                                print 'Null'
                                print
                            elif len(zhwiki_candidates_list) == 1:
                                zhwiki_entity = zhwiki_candidates_json[i][r][c]['candidates'][0]
                                print 'Only 1 candidate <' + zhwiki_entity + '>. Auto selection.'
                                print
                            else:
                                for k in range(len(zhwiki_candidates_list)):
                                    zhwiki_candidates_str += str(k)
                                    zhwiki_candidates_str += '. '
                                    zhwiki_candidates_str += zhwiki_candidates_list[k]
                                    zhwiki_candidates_str += '\n'

                                print zhwiki_candidates_str
                                candidate_index = input('Input the number before the entity you choose(If there is no referent entity, just input -1): ')
                                print

                                if int(candidate_index) == -1:
                                    zhwiki_entity = 'Null'
                                else:
                                    zhwiki_entity = zhwiki_candidates_json[i][r][c]['candidates'][int(candidate_index)]

                            dict_baidubaike['entity'] = baidubaike_entity
                            dict_hudongbaike['entity'] = hudongbaike_entity
                            dict_zhwiki['entity'] = zhwiki_entity
                            row_baidubaike.append(dict_baidubaike)
                            row_hudongbaike.append(dict_hudongbaike)
                            row_zhwiki.append(dict_zhwiki)
                        t_baidubaike.append(row_baidubaike)
                        t_hudongbaike.append(row_hudongbaike)
                        t_zhwiki.append(row_zhwiki)

                finally:
                    baidubaike_human_mark_json = json.dumps(t_baidubaike, ensure_ascii=False)
                    baidubaike_single_human_mark_file.write(baidubaike_human_mark_json)

                    hudongbaike_human_mark_json = json.dumps(t_hudongbaike, ensure_ascii=False)
                    hudongbaike_single_human_mark_file.write(hudongbaike_human_mark_json)

                    zhwiki_human_mark_json = json.dumps(t_zhwiki, ensure_ascii=False)
                    zhwiki_single_human_mark_file.write(zhwiki_human_mark_json)

                    if baidubaike_single_human_mark_file:
                        baidubaike_single_human_mark_file.close()

                    if hudongbaike_single_human_mark_file:
                        hudongbaike_single_human_mark_file.close()

                    if zhwiki_single_human_mark_file:
                        zhwiki_single_human_mark_file.close()

        finally:
            if baidubaike_candidates_file:
                baidubaike_candidates_file.close()

            if hudongbaike_candidates_file:
                hudongbaike_candidates_file.close()

            if zhwiki_candidates_file:
                zhwiki_candidates_file.close()

    def conbine(self):
        try:
            # baidubaike
            baidubaike_human_mark_file = open(self.baidubaike_total_human_mark_path, 'w')
            baidubaike_whole = []

            for i in range(self.table_quantity):
                human_mark_single_file_path = self.baidubaike_single_human_mark_path + str(i) + '.txt'
                human_mark_single_file = open(human_mark_single_file_path, 'r').read()
                human_mark_single_json = json.loads(human_mark_single_file)
                baidubaike_whole.append(human_mark_single_json)

            # hudongbaike
            hudongbaike_human_mark_file = open(self.hudongbaike_total_human_mark_path, 'w')
            hudongbaike_whole = []

            for i in range(self.table_quantity):
                human_mark_single_file_path = self.hudongbaike_single_human_mark_path + str(i) + '.txt'
                human_mark_single_file = open(human_mark_single_file_path, 'r').read()
                human_mark_single_json = json.loads(human_mark_single_file)
                hudongbaike_whole.append(human_mark_single_json)

            # zhwiki
            zhwiki_human_mark_file = open(self.zhwiki_total_human_mark_path, 'w')
            zhwiki_whole = []

            for i in range(self.table_quantity):
                human_mark_single_file_path = self.zhwiki_single_human_mark_path + str(i) + '.txt'
                human_mark_single_file = open(human_mark_single_file_path, 'r').read()
                human_mark_single_json = json.loads(human_mark_single_file)
                zhwiki_whole.append(human_mark_single_json)

        finally:
            baidubaike_human_mark_json = json.dumps(baidubaike_whole, ensure_ascii=False)
            baidubaike_human_mark_file.write(baidubaike_human_mark_json)

            hudongbaike_human_mark_json = json.dumps(hudongbaike_whole, ensure_ascii=False)
            hudongbaike_human_mark_file.write(hudongbaike_human_mark_json)

            zhwiki_human_mark_json = json.dumps(zhwiki_whole, ensure_ascii=False)
            zhwiki_human_mark_file.write(zhwiki_human_mark_json)

            if baidubaike_human_mark_file:
                baidubaike_human_mark_file.close()

            if hudongbaike_human_mark_file:
                hudongbaike_human_mark_file.close()

            if zhwiki_human_mark_file:
                zhwiki_human_mark_file.close()

    def split(self):
        try:
            # baidubaike
            baidubaike_human_mark_file = open(self.baidubaike_total_human_mark_path, 'r')
            baidubaike_human_mark = baidubaike_human_mark_file.read()
            baidubaike_human_mark_json = json.loads(baidubaike_human_mark, encoding='utf8')

            # hudongbaike
            hudongbaike_human_mark_file = open(self.hudongbaike_total_human_mark_path, 'r')
            hudongbaike_human_mark = hudongbaike_human_mark_file.read()
            hudongbaike_human_mark_json = json.loads(hudongbaike_human_mark, encoding='utf8')

            # zhwiki
            zhwiki_human_mark_file = open(self.zhwiki_total_human_mark_path, 'r')
            zhwiki_human_mark = zhwiki_human_mark_file.read()
            zhwiki_human_mark_json = json.loads(zhwiki_human_mark, encoding='utf8')


            for i in range(self.table_quantity):
                try:
                    baidubaike_single_human_mark_path = self.baidubaike_single_human_mark_path + str(i) + '.txt'
                    baidubaike_single_human_mark_file = open(baidubaike_single_human_mark_path, 'w')
                    baidubaike_single_human_mark_json = json.dumps(baidubaike_human_mark_json[i], ensure_ascii=False)
                    baidubaike_single_human_mark_file.write(baidubaike_single_human_mark_json)

                    hudongbaike_single_human_mark_path = self.hudongbaike_single_human_mark_path + str(i) + '.txt'
                    hudongbaike_single_human_mark_file = open(hudongbaike_single_human_mark_path, 'w')
                    hudongbaike_single_human_mark_json = json.dumps(hudongbaike_human_mark_json[i], ensure_ascii=False)
                    hudongbaike_single_human_mark_file.write(hudongbaike_single_human_mark_json)

                    zhwiki_single_human_mark_path = self.zhwiki_single_human_mark_path + str(i) + '.txt'
                    zhwiki_single_human_mark_file = open(zhwiki_single_human_mark_path, 'w')
                    zhwiki_single_human_mark_json = json.dumps(zhwiki_human_mark_json[i], ensure_ascii=False)
                    zhwiki_single_human_mark_file.write(zhwiki_single_human_mark_json)

                finally:
                    if baidubaike_single_human_mark_file:
                        baidubaike_single_human_mark_file.close()

                    if hudongbaike_single_human_mark_file:
                        hudongbaike_single_human_mark_file.close()

                    if zhwiki_single_human_mark_file:
                        zhwiki_single_human_mark_file.close()

        finally:
            if baidubaike_human_mark_file:
                baidubaike_human_mark_file.close()

            if hudongbaike_human_mark_file:
                hudongbaike_human_mark_file.close()

            if zhwiki_human_mark_file:
                zhwiki_human_mark_file.close()


