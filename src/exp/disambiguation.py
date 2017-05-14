# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 实验的第三步：单知识库候选实体消岐

import Levenshtein
import time
import copy
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import numpy as np
import os
import json
import jieba
from table import *


class EntityDisambiguationGraph(object):
    # kb_name: 知识库名称
    # table: 第i张表格，Table 类型对象
    # table_number: 表格的编号，即为 i
    # candidates: 当前表格中 mentions 的候选实体
    # graph_path: EDG 图片输出路径
    # edg_path: EDG 输出路径
    # infobox_property: 知识库的 infobox_property 文件，用于计算 IsRDF 特征和获取实体上下文
    # abstracts: 知识库的 abstracts 文件，用于获取实体的上下文
    # disambiguation_result_path: 消岐结果输出路径
    # mention_quantity: 当前表格中的 mention 数量
    # row_num: 当前表格的行数
    # col_num: 当前表格的列数
    # EDG: 当前表格及其候选实体生成的完成的 EDG
    # miniEDG: 去除 entity-entity Edge 的 EDG，为了更快速地画图
    # mention_node_begin: mention node 编号的开始
    # mention_node_end: mention node 编号的结束
    # entity_node_begin: entity node 编号的开始
    # entity_node_end: entity node 编号的结束
    # node_quantity: 所有节点的总数
    # alpha1, beta1, alpha2, beta2: 计算语义相似度时的参数
    # bonus: 实体节点上概率奖励增量，为其所在的候选实体集合中所有实体节点概率的平均值
    # A: 概率转移列表
    # r: 消岐结果概率列表
    def __init__(self, kb_name, table_number, table, candidates, graph_path, infobox_property, abstracts, disambiguation_output_path):
        self.kb_name = kb_name
        self.table_number = table_number
        self.table = table
        self.mention_quantity = table.mention_quantity
        self.row_num = table.row_num
        self.col_num = table.col_num
        self.candidates = candidates
        self.EDG = nx.Graph(number=str(table_number))
        self.miniEDG = nx.Graph(number=str(table_number))
        self.graph_path = graph_path
        self.edg_path = graph_path + 'edg' + str(table_number) + '.txt'
        self.infobox_property = infobox_property
        self.abstracts = abstracts
        self.disambiguation_result_path = disambiguation_output_path + str(table_number) + '.txt'
        self.mention_node_begin = 0
        self.mention_node_end = self.mention_quantity - 1
        self.entity_node_begin = self.mention_quantity
        self.entity_node_end = 0
        self.node_quantity = 0
        self.A = []
        self.r = []
        self.damping_factor = 0.5
        self.iterations = 500
        self.delta = 0.0001
        self.alpha1 = 0.5
        self.beta1 = 0.5
        self.alpha2 = 0.5
        self.beta2 = 0.5
        self.bonus = 0.0
        print 'Table ' + str(table_number)

    # 获取当前表格中一个 mention 的上下文，该 mention 位于第r行第c列，r与c都从0开始
    # r: mention 所处的行号
    # c: mention 所处的列号
    def get_mention_context(self, r, c):
        table = self.table
        mention_context = table.get_mention_context(r, c)
        return mention_context

    # 获取一个 entity e 的上下文，来自 abstract 和 infobox_property
    # e: entity 字符串
    def get_entity_context(self, e):
        entity_context = []

        # 从 infobox properties 中找实体的上下文
        infobox_property = self.infobox_property

        for rdf in infobox_property.readlines():
            rdf = rdf.strip('\n')

            # split
            split = rdf.split('> <')
            subject = split[0]
            object = split[2]

            # clean
            subject = subject[1:]
            object = object[:-1]

            if e == subject:
                object = object.decode('utf8')
                seg_list = jieba.lcut(object)   # unicode
                entity_context.extend(seg_list)

            if e == object:
                subject = subject.decode('utf8')
                seg_list = jieba.lcut(subject)  # unicode
                entity_context.extend(seg_list)

        # 从 abstracts 中找实体的上下文
        abstracts = self.abstracts
        seg_list = []

        for line in abstracts.readlines():
            line = line.strip('\n')

            # split
            split = line.split('> <')
            entity = split[0]
            abstract = split[1]

            # clean
            entity = entity[1:]
            abstract = abstract[:-1]

            if e == entity:
                seg_list = jieba.lcut(abstract)     # unicode

                if entity in seg_list:
                    seg_list.remove(entity)     # 移除摘要中的第一个出现的 entity，之后出现的 entity 都认为是上下文

                break

        entity_context.extend(seg_list)

        return entity_context   # unicode

    # 获取实体字符串的消岐义内容
    # entity: entity 字符串
    def get_entity_disambiguation(self, entity):
        disambiguation = ''

        # baidubaike
        if self.kb_name == 'baidubaike':        # 完整的实体 entity，包括消岐义内容 real_entity[disambiguation]
            split = entity.split('[')
            if len(split) == 2:
                disambiguation = split[1]
                disambiguation = disambiguation[:-1]

        if self.kb_name == 'hudongbaike':       # 完整的实体 entity，包括消岐义内容 real_entity [disambiguation] or real_entity[disambiguation]
            split = entity.split(' [')

            if len(split) == 1:
                newsplit = entity.split('[')
                if len(newsplit) == 2:
                    disambiguation = newsplit[1]
                    disambiguation = disambiguation[:-1]
            else:
                disambiguation = split[1]
                disambiguation = disambiguation[:-1]

        if self.kb_name == 'zhwiki':            # 完整的实体 entity，包括消岐义内容 real_entity (disambiguation)
            split = entity.split(' (')
            if len(split) == 2:
                disambiguation = split[1]
                disambiguation = disambiguation[:-1]

        return disambiguation

    # Building Entity Disambiguation Graph
    # mNode: mention node
    # eNode: entity node
    # meEdge: mention-entity edge
    # eeEdge: entity-entity edge
    # node probability: mention node probability 为初始权重值。entity node probability 在 iterative_probability_propagation() 中计算
    # edge probability: 边两端节点间的语义相似度。有2种边，mention-entity edge 和 entity-entity edge
    def build_entity_disambiguation_graph(self):
        print 'Building Entity Disambiguation Graph......',
        EDG = self.EDG
        table = self.table
        candidates = self.candidates
        nRow = self.row_num
        nCol = self.col_num
        i = self.table_number
        mention_quantity = self.mention_quantity
        mention_node_initial_importance = float(1)/mention_quantity

        # mention node 编号范围为 [0, mention_quantity - 1]
        # entity node 编号范围为 [mention_quantity, entity_node_end]
        # 所有节点的编号范围为 [0, entity_node_end]
        mention_counter = 0
        entity_counter = mention_quantity

        # 逐行逐列遍历一张表格中的每个单元格
        # i: table number
        # r: row number
        # c: column number
        for r in range(nRow):
            if r == 0:  # 表头不作为 EDG 中的节点
                continue

            for c in range(nCol):
                mention = table.get_cell(r, c)                          # unicode
                mention_candidates = candidates[r][c]['candidates']     # unicode
                candidates_quantity = len(mention_candidates)
                candidate_index = 0

                if candidates_quantity == 0:
                    flag_NIL = True
                else:
                    flag_NIL = False

                # 在 EDG 中添加 mention node
                # ranking: [(entity node index i, the probability for the node i to be the referent entity of the mention)] 候选实体根据概率逆序排列的列表
                EDG.add_node(mention_counter, type='mNode', mention=mention, NIL=flag_NIL, table=i, row=r, column=c, ranking=[], probability=float(mention_node_initial_importance), context=[])
                EDG.node[mention_counter]['label'] = 'mention: ' + EDG.node[mention_counter]['mention']
                EDG.node[mention_counter]['context'] = self.get_mention_context(r, c)

                if flag_NIL == False:
                    # 在 EDG 中添加 entity node
                    # candidate: 候选实体字符串
                    # mNode_index: entity node 相邻的唯一一个 mention node 的编号
                    # disambiguation: 实体名称中的消岐义部分 entity [disambiguation]
                    for candidate in mention_candidates:
                        candidate_index += 1
                        EDG.add_node(entity_counter, type='eNode', candidate=candidate, index=candidate_index, mNode_index=mention_counter, probability=float(0), context=[], disambiguation='')
                        # EDG.node[entity_counter]['label'] = 'candidate' + str(EDG.node[entity_counter]['index']) + ': ' + EDG.node[entity_counter]['candidate']
                        EDG.node[entity_counter]['context'] = self.get_entity_context(candidate)
                        EDG.node[entity_counter]['disambiguation'] = self.get_entity_disambiguation(candidate)

                        # 在 EDG 中添加 mention-entity edge
                        EDG.add_edge(mention_counter, entity_counter, type='meEdge', probability=float(0))

                        entity_counter += 1
                mention_counter += 1

        self.entity_node_end = entity_counter - 1
        self.node_quantity = self.entity_node_end + 1
        self.miniEDG = copy.deepcopy(EDG)

        # 在 EDG 中添加 entity-entity edge
        for p in range(self.entity_node_begin, self.entity_node_end + 1):
            for q in range(self.entity_node_begin, self.entity_node_end + 1):
                if p < q:
                    EDG.add_edge(p, q, type='eeEdge', probability=float(0))
                    EDG.edge[p][q]['label'] = str(EDG.edge[p][q]['probability'])

        self.EDG = EDG
        print 'Done!'

    def save_entity_disambiguation_graph(self):
        print 'Saving Entity Disambiguation Graph......',
        EDG = self.EDG
        nx.write_gpickle(EDG, self.edg_path)
        print 'Done!'

    def load_entity_disambiguation_graph(self):
        self.EDG = nx.read_gpickle(self.edg_path)

    # 画出来的 EDG 图不包含 entity-entity Edge，否则时间开销太大
    def draw_entity_disambiguation_graph(self):
        print 'Drawing Entity Disambiguation Graph......',
        graph_name = self.graph_path + 'edg' + str(self.table_number)
        write_dot(self.miniEDG, graph_name + '.dot')
        os.system('dot -Tsvg ' + graph_name + '.dot' + ' -o ' + graph_name + '.svg')
        print 'Done!'

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

    # 计算 mention 和 entity 之间的字符串相似度特征 (String Similarity Feature)
    # m: mention node index
    # e: entity node index
    def strSim(self, m, e):
        mention = self.EDG.node[m]['mention']       # unicode
        entity = self.EDG.node[e]['candidate']      # unicode

        if self.kb_name == 'baidubaike':            # 完整的实体，包括消岐义内容 real_entity[disambiguation]
            split = entity.split('[')
            real_entity = split[0]                  # 真实的实体 (unicode)，去除了消岐义内容 real_entity

        if self.kb_name == 'hudongbaike':           # 完整的实体，包括消岐义内容 real_entity [disambiguation] or real_entity[disambiguation]
            split = entity.split(' [')

            if len(split) == 1:
                entity = split[0]
                newsplit = entity.split('[')
                real_entity = newsplit[0]           # 真实的实体 (unicode)，去除了消岐义内容 real_entity
            else:
                real_entity = split[0]              # 真实的实体 (unicode)，去除了消岐义内容 real_entity

        if self.kb_name == 'zhwiki':                # 完整的实体，包括消岐义内容 real_entity (disambiguation)
            split = entity.split(' (')
            real_entity = split[0]                  # 真实的实体 (unicode)，去除了消岐义内容 real_entity

        string_similarity = self.string_similarity(mention, real_entity)
        return string_similarity

    # Jaccard Similarity
    # x: string list
    # y: string list
    def jaccard_similarity(self, x, y):
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        jaccard_similarity = intersection_cardinality / float(union_cardinality)
        return jaccard_similarity

    # 计算 mention 和 entity 之间的上下文相似度特征 (Mention-Entity Context Similarity Feature)
    # m: mention node index
    # e: entity node index
    def contSim_me(self, m, e):
        mention_context = self.EDG.node[m]['context']
        entity_context = self.EDG.node[e]['context']

        if len(entity_context) == 0:
            context_similarity_me = 0.0
            return context_similarity_me

        context_similarity_me = self.jaccard_similarity(mention_context, entity_context)
        return context_similarity_me

    # 计算 mention 和 entity 之间的语义相似度 (Mention-Entity Semantic Relatedness)
    # m: mention node index
    # e: entity node index
    def SR_me(self, m, e):
        alpha1 = self.alpha1
        beta1 = self.beta1
        sr_me = 0.99 * (alpha1 * self.strSim(m, e) + beta1 * self.contSim_me(m, e)) + 0.01
        return sr_me

    # 计算 mention node 和其所有相邻 entity node 之间的语义相似度之和
    # m: mention node index
    def SR_me_star(self, m):
        sr_me_star = 0.0

        if self.EDG.node[m]['NIL'] == True:
            return sr_me_star
        else:
            candidates = self.EDG.neighbors(m)

            for e in candidates:
                sr_me_star += self.EDG.edge[m][e]['probability']

            return sr_me_star

    # 计算 2 entities 之间的三元组关系特征 (Triple Relation Feature)
    # ???: e1 和 e2 存在于同一个 RDF 中是否需要存在于不同部分
    # e1: entity1 node index
    # e2: entity2 node index
    def IsRDF(self, e1, e2):
        is_rdf = 0
        entity1 = self.EDG.node[e1]['candidate']
        entity2 = self.EDG.node[e2]['candidate']

        infobox_property = self.infobox_property

        for rdf in infobox_property.readlines():
            rdf = rdf.strip('\n')

            if entity1 in rdf and entity2 in rdf:
                is_rdf = 1
                break

        return is_rdf

    # 计算 2 entities 之间的上下文相似度特征 (Entity-Entity Context Similarity Feature)
    # e1: entity1 node index
    # e2: entity2 node index
    def contSim_ee(self, e1, e2):
        entity1_context = self.EDG.node[e1]['context']
        entity2_context = self.EDG.node[e2]['context']

        if len(entity1_context) == 0 or len(entity2_context) == 0:
            context_similarity_ee = 0.0
            return context_similarity_ee

        context_similarity_ee = self.jaccard_similarity(entity1_context, entity2_context)
        return context_similarity_ee

    # 计算 2 entities 之间的语义相似度 (Entity-Entity Semantic Relatedness)
    # e1: entity1 node index
    # e2: entity2 node index
    def SR_ee(self, e1, e2):
        alpha2 = self.alpha2
        beta2 = self.alpha2
        sr_ee = 0.99 * (alpha2 * self.IsRDF(e1, e2) + beta2 * self.contSim_ee(e1, e2)) + 0.01
        return sr_ee

    # 计算 entity node 和其相邻的唯一一个 mention node 之间的语义相似度
    # e: entity node index
    def SR_em(self, e):
        m = self.EDG.node[e]['mNode_index']
        sr_em = self.EDG.edge[m][e]['probability']
        return sr_em

    # 计算 entity node 和其所有相邻 entity node 之间的语义相似度之和
    # e: entity node index
    def SR_ee_star(self, e):
        sr_ee_star = 0.0

        m = self.EDG.node[e]['mNode_index']
        sr_me = self.EDG.edge[m][e]['probability']

        entities = self.EDG.neighbors(e)

        for ee in entities:
            sr_ee_star += self.EDG.edge[e][ee]['probability']

        sr_ee_star -= sr_me

        return sr_ee_star

    # Computing EL Impact Factors
    def compute_el_impact_factors(self):
        print 'Computing the EL Impact Factors......',
        EDG = self.EDG

        # compute semantic relatedness between mentions and entities
        # k: mention node 编号
        # i: entity node 编号
        for k in range(self.mention_node_begin, self.mention_node_end + 1):
            if EDG.node[k]['NIL'] == True:
                continue

            candidates = EDG.neighbors(k)

            for i in candidates:
                EDG.edge[k][i]['probability'] = self.SR_me(k, i)

        # compute semantic relatedness between entities
        # p: entity1 node 编号
        # q: entity2 node 编号
        for p in range(self.entity_node_begin, self.entity_node_end + 1):
            for q in range(self.entity_node_begin, self.entity_node_end + 1):
                if p < q:
                    EDG.edge[p][q]['probability'] = self.SR_ee(p, q)

        self.EDG = EDG
        print 'Done!'

    # Iterative Probability Propagation
    # 计算 entity node probability (该 entity 成为 mention 的对应实体的概率)
    def iterative_probability_propagation(self):
        print 'Iterative Probability Propagation (Iteration Limit: ' + str(self.iterations) + ', Delta: ' + str(self.delta) + ', Damping Factor: ' + str(self.damping_factor) + ')......',
        EDG = self.EDG
        n = self.node_quantity
        damping_factor = self.damping_factor
        iterations = self.iterations
        delta = self.delta
        A = [[0.0 for col in range(n)] for row in range(n)]
        E = [[1.0 for col in range(n)] for row in range(n)]
        r = [0.0 for i in range(n)]
        flag_convergence = False

        # compute A[i][j]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue

                i_type = EDG.node[i]['type']
                j_type = EDG.node[j]['type']

                if i_type == 'mNode' and j_type == 'mNode':
                    continue

                if i_type == 'mNode' and j_type == 'eNode':
                    if EDG.node[i]['NIL'] == True:
                        continue
                    else:
                        if EDG.has_edge(i, j) == False:
                            continue
                        else:
                            A[i][j] = EDG.edge[i][j]['probability'] / self.SR_me_star(i)

                if i_type == 'eNode' and j_type == 'mNode':
                    if EDG.node[j]['NIL'] == True:
                        continue
                    else:
                        if EDG.has_edge(i, j) == False:
                            continue
                        else:
                            A[i][j] = A[j][i]

                if i_type == 'eNode' and j_type == 'eNode':
                    A[i][j] = (1.0 - self.SR_em(i)) * EDG.edge[i][j]['probability'] / self.SR_ee_star(i)

        self.A = A

        # initialize r(i)
        # epoch 0
        for i in range(n):
            if i < self.mention_quantity:
                r[i] = 1.0 / self.mention_quantity  # mNode
            else:
                r[i] = 0.0  # eNode

        matrix_r = np.matrix(r).T
        matrix_A = np.matrix(A)
        matrix_E = np.matrix(E)

        # update r(i)
        for epoch in range(1, iterations + 1):
            matrix_r_next = ((1.0 - damping_factor) * (matrix_E / n) + damping_factor * matrix_A) * matrix_r

            r_list = matrix_r.tolist()
            r_next_list = matrix_r_next.tolist()
            max_difference = 0.0

            for i in range(n):
                if EDG.node[i]['type'] == 'eNode':
                    difference = abs(r_list[i][0] - r_next_list[i][0])

                    if difference > max_difference:
                        max_difference = difference

            if max_difference <= delta:
                print 'At Epoch ' + str(epoch) + ' Convergence is Reached!'
                matrix_r = matrix_r_next
                flag_convergence = True
                break

            matrix_r = matrix_r_next

        r_list = matrix_r.tolist()

        for i in range(n):
            r[i] = r_list[i][0]

        if flag_convergence == False:
            print 'After Epoch ' + str(iterations) + ' Iterative Probability Propagation is Done!'

        self.r = r
        self.EDG = EDG

    # 给 mention 的候选实体排名
    def rank_candidates(self):
        print 'Ranking candidates......',
        EDG = self.EDG
        r = self.r

        for i in range(self.mention_node_begin, self.mention_node_end + 1):
            if EDG.node[i]['NIL'] == True:
                continue

            mention = EDG.node[i]['mention']
            mention_context = EDG.node[i]['context']
            candidates = EDG.neighbors(i)
            ranking = []

            self.bonus = 0.0
            for e in candidates:
                self.bonus += r[e]
            self.bonus /= len(candidates)

            for e in candidates:
                entity = EDG.node[e]['candidate']
                disambiguation = EDG.node[e]['disambiguation']
                probability = r[e]

                if entity == mention:
                    probability += self.bonus           # 候选实体与 mention 完全相同，奖励该候选实体

                for c in mention_context:
                    if c in disambiguation:
                        probability += 2 * self.bonus    # mention 的上下文中元素出现在候选实体的消岐义内容中，奖励该候选实体

                r[e] = probability
                tuple = (e, probability)    # (实体节点编号，实体成为 mention 的对应实体的概率)
                ranking.append(tuple)

            # 将实体结果的概率归一化
            max = 0.0
            for e in candidates:
                if r[e] > max:
                    max = r[e]

            for e in candidates:
                r[e] /= max

            newranking = []
            for t in ranking:
                t = list(t)
                e = t[0]
                p = t[1] / max
                tuple = (e, p)
                newranking.append(tuple)

            newranking.sort(key=lambda x: x[1], reverse=True)  # newranking 根据概率逆序排序，下标越小概率越大
            EDG.node[i]['ranking'] = newranking

        # 计算 eNode 上的概率 并 打上标签
        for p in range(self.entity_node_begin, self.entity_node_end + 1):
            EDG.node[p]['probability'] = r[p]
            self.miniEDG.node[p]['label'] = 'candidate' + str(EDG.node[p]['index']) + ': ' + EDG.node[p]['candidate'] + '\n' + str(EDG.node[p]['probability'])

        self.EDG = EDG
        print 'Done!'

    # 挑选出 mention 的候选实体中概率最高的一个 entity
    # 将消岐后的结果文件存储于 disambiguation_output_path
    def pick_entity(self):
        print 'Picking the referent entity......',
        EDG = self.EDG
        table = self.table
        nRow = self.row_num
        nCol = self.col_num
        i = self.mention_node_begin
        t = []

        for m in range(nRow):
            row = []
            for n in range(nCol):
                dict = {}

                if m == 0:
                    dict['header'] = table.get_cell(m, n)
                else:
                    mention = EDG.node[i]['mention']

                    if EDG.node[i]['NIL'] == True:
                        entity = 'Null'
                    else:
                        eNode_index = EDG.node[i]['ranking'][0][0]
                        entity = EDG.node[eNode_index]['candidate']

                    dict['mention'] = mention
                    dict['entity'] = entity
                    i += 1

                row.append(dict)
            t.append(row)

        try:
            disambiguation_file = open(self.disambiguation_result_path, 'w')

        finally:
            disambiguation_result = json.dumps(t, ensure_ascii=False)
            disambiguation_file.write(disambiguation_result)

            if disambiguation_file:
                disambiguation_file.close()

        print 'Done!'


class Disambiguation(object):
    # table_name: 表格文件的名称
    # table_path: 表格文件的路径
    # kb_name: 知识库的名称
    # candidate_name: 候选实体文件的名称
    # candidate_path: 候选实体文件的路径
    # graph_path: Entity Disambiguation Graph 存储路径
    # disambiguation_output_path: 消岐结果文件的路径
    # infobox_property_path: 知识库的 infobox_property 文件路径
    # abstracts_path: 知识库的 abstracts 文件路径
    def __init__(self, table_name, table_path, kb_name, candidate_name, candidate_path, graph_path, disambiguation_output_path, infobox_property_path, abstracts_path):
        table_manager = TableManager(table_path)
        self.tables = table_manager.get_tables()  # tables 是 Table 类型数组
        self.table_name = table_name
        self.table_path = table_path
        self.table_quantity = table_manager.table_quantity
        self.kb_name = kb_name
        self.candidate_name = candidate_name
        self.candidate_path = candidate_path
        self.graph_path = graph_path
        self.disambiguation_output_path = disambiguation_output_path
        self.infobox_property_path = infobox_property_path
        self.abstracts_path = abstracts_path

    def disambiguation(self):
        # baidubaike
        if self.kb_name == "baidubaike":
            try:
                kb_name = self.kb_name
                tables = self.tables
                baidubaike_graph_path = self.graph_path
                baidubaike_disambiguation_output_path = self.disambiguation_output_path
                baidubaike_candidate_file = open(self.candidate_path, 'r')
                baidubaike_candidate = baidubaike_candidate_file.read()
                baidubaike_candidate_json = json.loads(baidubaike_candidate, encoding='utf8')    # kb_candidate[nTable][nRow][nCol] = dict{'mention': m, 'candidates': []}
                baidubaike_infobox_property = open(self.infobox_property_path, 'r')
                baidubaike_abstracts = open(self.abstracts_path, 'r')

                # i: 第i张表格，从0开始
                for i in range(self.table_quantity):
                    table = tables[i]
                    candidates = baidubaike_candidate_json[i]

                    EDG_master = EntityDisambiguationGraph(kb_name, i, table, candidates, baidubaike_graph_path, baidubaike_infobox_property, baidubaike_abstracts, baidubaike_disambiguation_output_path)

                    time1 = time.time()

                    EDG_master.build_entity_disambiguation_graph()
                    EDG_master.compute_el_impact_factors()
                    EDG_master.iterative_probability_propagation()
                    EDG_master.rank_candidates()
                    EDG_master.pick_entity()
                    EDG_master.save_entity_disambiguation_graph()
                    EDG_master.draw_entity_disambiguation_graph()

                    time2 = time.time()
                    print 'Consumed Time: ' + str(time2 - time1) + ' s'
                    print

            finally:
                if baidubaike_candidate_file:
                    baidubaike_candidate_file.close()

                if baidubaike_infobox_property:
                    baidubaike_infobox_property.close()

                if baidubaike_abstracts:
                    baidubaike_abstracts.close()


        # hudongbaike
        if self.kb_name == "hudongbaike":
            try:
                kb_name = self.kb_name
                tables = self.tables
                hudongbaike_graph_path = self.graph_path
                hudongbaike_disambiguation_output_path = self.disambiguation_output_path
                hudongbaike_candidate_file = open(self.candidate_path, 'r')
                hudongbaike_candidate = hudongbaike_candidate_file.read()
                hudongbaike_candidate_json = json.loads(hudongbaike_candidate, encoding='utf8')    # kb_candidate[nTable][nRow][nCol] = dict{'mention': m, 'candidates': []}
                hudongbaike_infobox_property = open(self.infobox_property_path, 'r')
                hudongbaike_abstracts = open(self.abstracts_path, 'r')

                # i: 第i张表格，从0开始
                for i in range(self.table_quantity):
                    table = tables[i]
                    candidates = hudongbaike_candidate_json[i]

                    EDG_master = EntityDisambiguationGraph(kb_name, i, table, candidates, hudongbaike_graph_path, hudongbaike_infobox_property, hudongbaike_abstracts, hudongbaike_disambiguation_output_path)

                    time1 = time.time()

                    EDG_master.build_entity_disambiguation_graph()
                    EDG_master.compute_el_impact_factors()
                    EDG_master.iterative_probability_propagation()
                    EDG_master.rank_candidates()
                    EDG_master.pick_entity()
                    EDG_master.save_entity_disambiguation_graph()
                    EDG_master.draw_entity_disambiguation_graph()

                    time2 = time.time()
                    print 'Consumed Time: ' + str(time2 - time1) + ' s'
                    print

            finally:
                if hudongbaike_candidate_file:
                    hudongbaike_candidate_file.close()

                if hudongbaike_infobox_property:
                    hudongbaike_infobox_property.close()

                if hudongbaike_abstracts:
                    hudongbaike_abstracts.close()


        # zhwiki
        if self.kb_name == "zhwiki":
            try:
                kb_name = self.kb_name
                tables = self.tables
                zhwiki_graph_path = self.graph_path
                zhwiki_disambiguation_output_path = self.disambiguation_output_path
                zhwiki_candidate_file = open(self.candidate_path, 'r')
                zhwiki_candidate = zhwiki_candidate_file.read()
                zhwiki_candidate_json = json.loads(zhwiki_candidate, encoding='utf8')    # kb_candidate[nTable][nRow][nCol] = dict{'mention': m, 'candidates': []}
                zhwiki_infobox_property = open(self.infobox_property_path, 'r')
                zhwiki_abstracts = open(self.abstracts_path, 'r')

                # i: 第i张表格，从0开始
                for i in range(self.table_quantity):
                    table = tables[i]
                    candidates = zhwiki_candidate_json[i]

                    EDG_master = EntityDisambiguationGraph(kb_name, i, table, candidates, zhwiki_graph_path, zhwiki_infobox_property, zhwiki_abstracts, zhwiki_disambiguation_output_path)

                    time1 = time.time()

                    EDG_master.build_entity_disambiguation_graph()
                    EDG_master.compute_el_impact_factors()
                    EDG_master.iterative_probability_propagation()
                    EDG_master.rank_candidates()
                    EDG_master.pick_entity()
                    EDG_master.save_entity_disambiguation_graph()
                    EDG_master.draw_entity_disambiguation_graph()

                    time2 = time.time()
                    print 'Consumed Time: ' + str(time2 - time1) + ' s'
                    print

            finally:
                if zhwiki_candidate_file:
                    zhwiki_candidate_file.close()

                if zhwiki_infobox_property:
                    zhwiki_infobox_property.close()

                if zhwiki_abstracts:
                    zhwiki_abstracts.close()


