# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 实验的第一步：原始知识库数据预处理
# 从原始nt文件中抽取实体及其对应的url，并转码

from urllib import unquote

class Preprocess(object):
    # kb_name: 知识库的名称
    # kb_labels_path: 知识库 label 文件的路径
    # kb_entity_quantity: 知识库中实体的数量
    # entity_url_output_path: 处理好的实体以及url数据的输出路径
    # kb_infobox_properties_path: 知识库 infobox_properties 文件路径，用于检测2个实体是否在同一个 RDF 三元组中，以及获取实体的上下文
    # infobox_properties_output_path: 从 infobox_properties 文件中抽取出的 RDF 三元组数据的输出路径
    # kb_infobox_properties_quantity: 知识库中 infobox_properties 的数量
    # kb_abstracts_path: 知识库 abstracts 文件路径，用于获取实体的上下文
    # abstracts_output_path: 从 abstracts 文件中抽取出的数据
    # kb_abstracts_quantity: 知识库中 abstracts 的数量
    # synonym_path: 由 BabelNet 生成的实体同义词文件的路径
    # entity_synonym_output_path: 实体及其同义词的联合文件输出路径
    # synonym_quantity: 知识库中有同义词的实体数量
    def __init__(self, kb_name, kb_labels_path, entity_url_output_path, kb_infobox_properties_path, infobox_properties_output_path, kb_abstracts_path, abstracts_output_path, synonym_path, entity_synonym_output_path):
        self.kb_name = kb_name
        self.kb_labels_path = kb_labels_path
        self.entity_url_output_path = entity_url_output_path
        self.kb_entity_quantity = 0
        self.kb_infobox_properties_path = kb_infobox_properties_path
        self.infobox_properties_output_path = infobox_properties_output_path
        self.kb_infobox_properties_quantity = 0
        self.kb_abstracts_path = kb_abstracts_path
        self.abstracts_output_path = abstracts_output_path
        self.kb_abstracts_quantity = 0
        self.synonym_path = synonym_path
        self.entity_synonym_output_path = entity_synonym_output_path
        self.synonym_quantity = 0

    # 从 labels 文件中抽取知识库的实体
    def extract_entity(self):
        # baidubaike
        if self.kb_name == 'baidubaike':
            try:
                baidubaike_labels = open(self.kb_labels_path, 'r')
                baidubaike_entities = open(self.entity_url_output_path, 'a')
                baidubaike_entity_counter = 0
                baidubaike_entity_sum = 4265127

                for rdf in baidubaike_labels.readlines():
                    rdf = rdf.strip('\n')

                    # split
                    firstsplit = rdf.split('> <')
                    url = firstsplit[0]
                    rdf_entity = firstsplit[1]

                    secondsplit = rdf_entity.split('> "')
                    entity = secondsplit[1]

                    # clean
                    url = url[1:]
                    entity = entity[:-7]
                    entity = entity.replace('\'', '')

                    # convert entity
                    entity = eval("u'%s'" %(entity)).encode('utf8')

                    entity_url = '<' + entity + '> <' + url + '>\n'

                    baidubaike_entities.write(entity_url)

            finally:
                self.kb_entity_quantity = baidubaike_entity_counter

                if baidubaike_labels:
                    baidubaike_labels.close()

                if baidubaike_entities:
                    baidubaike_entities.close()


        # hudongbaike
        if self.kb_name == 'hudongbaike':
            try:
                hudongbaike_labels = open(self.kb_labels_path, 'r')
                hudongbaike_entities = open(self.entity_url_output_path, 'a')
                hudongbaike_entity_counter = 0
                hudongbaike_entity_sum = 3299288

                for rdf in hudongbaike_labels.readlines():
                    hudongbaike_entity_counter += 1
                    rdf = rdf.strip('\n')

                    # split
                    firstsplit = rdf.split('> <')
                    url = firstsplit[0]
                    rdf_entity = firstsplit[1]

                    secondsplit = rdf_entity.split('> "')
                    entity = secondsplit[1]

                    # clean
                    url = url[1:]
                    entity = entity[:-7]
                    entity = entity.replace('\'', '')

                    # convert entity
                    entity = eval("u'%s'" % (entity)).encode('utf8')

                    entity_url = '<' + entity + '> <' + url + '>\n'
                    hudongbaike_entities.write(entity_url)

            finally:
                self.kb_entity_quantity = hudongbaike_entity_counter

                if hudongbaike_labels:
                    hudongbaike_labels.close()

                if hudongbaike_entities:
                    hudongbaike_entities.close()


        # zhwiki
        if self.kb_name == 'zhwiki':
            try:
                zhwiki_labels = open(self.kb_labels_path, 'r')
                zhwiki_entities = open(self.entity_url_output_path, 'a')
                zhwiki_entity_counter = 0
                zhwiki_entity_sum = 830734

                for rdf in zhwiki_labels.readlines():
                    zhwiki_entity_counter += 1
                    rdf = rdf.strip('\n')

                    # split
                    firstsplit = rdf.split('> <')
                    url = firstsplit[0]
                    rdf_entity = firstsplit[1]

                    secondsplit = rdf_entity.split('> "')
                    entity = secondsplit[1]

                    # clean
                    url = url[1:]
                    entity = entity[:-6]
                    entity = entity.replace('\'', '')

                    # convert entity
                    entity = eval("u'%s'" %(entity)).encode('utf8')

                    entity_url = '<' + entity + '> <' + url + '>\n'
                    zhwiki_entities.write(entity_url)

            finally:
                self.kb_entity_quantity = zhwiki_entity_counter

                if zhwiki_labels:
                    zhwiki_labels.close()

                if zhwiki_entities:
                    zhwiki_entities.close()

    # 从 infobox_properties 文件中抽取 RDF 数据，用来：
    # 1. 检测2个实体是否存在于同一个 RDF 中
    # 2. 获取实体的上下文
    def extract_infobox_properties(self):
        # baidubaike
        if self.kb_name == 'baidubaike':
            try:
                baidubaike_infobox_properties = open(self.kb_infobox_properties_path, 'r')
                baidubaike_isrdf = open(self.infobox_properties_output_path, 'a')
                baidubaike_infobox_properties_counter = 0
                baidubaike_infobox_properties_sum = 766807

                for rdf in baidubaike_infobox_properties.readlines():
                    baidubaike_infobox_properties_counter += 1
                    rdf = rdf.strip('\n')

                    # split
                    firstsplit = rdf.split('> <')
                    rdf0 = firstsplit[0]

                    secondsplit = firstsplit[1].split('> "')
                    rdf1 = secondsplit[0]
                    rdf2 = secondsplit[1]

                    # clean
                    rdf0 = rdf0[1:]
                    rdf0 = rdf0.replace('http://zhishi.me/baidubaike/resource/', '')

                    rdf1 = rdf1.replace('http://zhishi.me/baidubaike/property/', '')
                    rdf2 = rdf2[:-7]

                    # convert
                    rdf0 = unquote(rdf0)
                    rdf1 = unquote(rdf1)

                    try:
                        rdf2 = eval("u'%s'" % (rdf2)).encode('utf8')
                        new_rdf = '<' + rdf0 + '> <' + rdf1 + '> <' + rdf2 + '>\n'

                    except:
                        new_rdf = '<' + rdf0 + '> <' + rdf1 + '> <' + rdf2 + '>\n'

                    baidubaike_isrdf.write(new_rdf)

            finally:
                self.kb_infobox_properties_quantity = baidubaike_infobox_properties_counter

                if baidubaike_infobox_properties:
                    baidubaike_infobox_properties.close()

                if baidubaike_isrdf:
                    baidubaike_isrdf.close()


        # hudongbaike
        if self.kb_name == 'hudongbaike':
            try:
                hudongbaike_infobox_properties = open(self.kb_infobox_properties_path, 'r')
                hudongbaike_isrdf = open(self.infobox_properties_output_path, 'a')
                hudongbaike_infobox_properties_counter = 0
                hudongbaike_infobox_properties_sum = 4609228

                for rdf in hudongbaike_infobox_properties.readlines():
                    hudongbaike_infobox_properties_counter += 1
                    rdf = rdf.strip('\n')

                    # split
                    firstsplit = rdf.split('> <')
                    rdf0 = firstsplit[0]

                    secondsplit = firstsplit[1].split('> "')
                    rdf1 = secondsplit[0]
                    rdf2 = secondsplit[1]

                    # clean
                    rdf0 = rdf0[1:]
                    rdf0 = rdf0.replace('http://zhishi.me/hudongbaike/resource/', '')

                    rdf1 = rdf1.replace('http://zhishi.me/hudongbaike/property/', '')
                    rdf2 = rdf2[:-7]

                    # convert
                    rdf0 = unquote(rdf0)
                    rdf1 = unquote(rdf1)

                    try:
                        rdf2 = eval("u'%s'" % (rdf2)).encode('utf8')
                        new_rdf = '<' + rdf0 + '> <' + rdf1 + '> <' + rdf2 + '>\n'

                    except:
                        new_rdf = '<' + rdf0 + '> <' + rdf1 + '> <' + rdf2 + '>\n'

                    hudongbaike_isrdf.write(new_rdf)

            finally:
                self.kb_infobox_properties_quantity = hudongbaike_infobox_properties_counter

                if hudongbaike_infobox_properties:
                    hudongbaike_infobox_properties.close()

                if hudongbaike_isrdf:
                    hudongbaike_isrdf.close()


        # zhwiki
        if self.kb_name == 'zhwiki':
            try:
                zhwiki_infobox_properties = open(self.kb_infobox_properties_path, 'r')
                zhwiki_isrdf = open(self.infobox_properties_output_path, 'a')
                zhwiki_infobox_properties_counter = 0
                zhwiki_infobox_properties_sum = 120509

                for rdf in zhwiki_infobox_properties.readlines():
                    zhwiki_infobox_properties_counter += 1
                    rdf = rdf.strip('\n')

                    # split
                    firstsplit = rdf.split('> <')
                    rdf0 = firstsplit[0]

                    secondsplit = firstsplit[1].split('> "')
                    rdf1 = secondsplit[0]
                    rdf2 = secondsplit[1]

                    # clean
                    rdf0 = rdf0[1:]
                    rdf0 = rdf0.replace('http://zhishi.me/zhwiki/resource/', '')

                    rdf1 = rdf1.replace('http://zhishi.me/zhwiki/property/', '')
                    rdf2 = rdf2[:-6]

                    # convert
                    rdf0 = unquote(rdf0)

                    try:
                        rdf1 = eval("u'%s'" % (rdf1)).encode('utf8')
                        rdf2 = eval("u'%s'" % (rdf2)).encode('utf8')
                        new_rdf = '<' + rdf0 + '> <' + rdf1 + '> <' + rdf2 + '>\n'

                    except:
                        new_rdf = '<' + rdf0 + '> <' + rdf1 + '> <' + rdf2 + '>\n'

                    zhwiki_isrdf.write(new_rdf)

            finally:
                self.kb_infobox_properties_quantity = zhwiki_infobox_properties_counter

                if zhwiki_infobox_properties:
                    zhwiki_infobox_properties.close()

                if zhwiki_isrdf:
                    zhwiki_isrdf.close()

    # 从 abstracts 文件中抽取 abstract 数据，用于获取实体的上下文
    def extract_abstracts(self):
        # baidubaike
        if self.kb_name == 'baidubaike':
            try:
                baidubaike_abstracts_file = open(self.kb_abstracts_path, 'r')
                baidubaike_abstracts_output_file = open(self.abstracts_output_path, 'a')
                baidubaike_abstracts_counter = 0
                baidubaike_abstracts_sum = 553302

                for line in baidubaike_abstracts_file.readlines():
                    baidubaike_abstracts_counter += 1
                    line = line.strip('\n')

                    # split
                    firstsplit = line.split('> <')
                    entity = firstsplit[0]

                    secondsplit = firstsplit[1].split('> "')
                    abstract = secondsplit[1]

                    # clean
                    entity = entity[1:]
                    entity = entity.replace('http://zhishi.me/baidubaike/resource/', '')
                    abstract = abstract[:-7]

                    # convert
                    entity = unquote(entity)

                    try:
                        abstract = eval("u'%s'" % (abstract)).encode('utf8')
                        entity_abstract = '<' + entity + '> <' + abstract + '>\n'

                    except:
                        entity_abstract = '<' + entity + '> <' + abstract + '>\n'

                    baidubaike_abstracts_output_file.write(entity_abstract)

            finally:
                self.kb_abstracts_quantity = baidubaike_abstracts_counter

                if baidubaike_abstracts_file:
                    baidubaike_abstracts_file.close()

                if baidubaike_abstracts_output_file:
                    baidubaike_abstracts_output_file.close()

        # hudongbaike
        if self.kb_name == 'hudongbaike':
            try:
                hudongbaike_abstracts_file = open(self.kb_abstracts_path, 'r')
                hudongbaike_abstracts_output_file = open(self.abstracts_output_path, 'a')
                hudongbaike_abstracts_counter = 0
                hudongbaike_abstracts_sum = 1625993

                for line in hudongbaike_abstracts_file.readlines():
                    hudongbaike_abstracts_counter += 1
                    line = line.strip('\n')

                    # split
                    firstsplit = line.split('> <')
                    entity = firstsplit[0]

                    secondsplit = firstsplit[1].split('> "')
                    abstract = secondsplit[1]

                    # clean
                    entity = entity[1:]
                    entity = entity.replace('http://zhishi.me/hudongbaike/resource/', '')
                    abstract = abstract[:-7]

                    # convert
                    entity = unquote(entity)

                    try:
                        abstract = eval("u'%s'" % (abstract)).encode('utf8')
                        entity_abstract = '<' + entity + '> <' + abstract + '>\n'

                    except:
                        entity_abstract = '<' + entity + '> <' + abstract + '>\n'

                    hudongbaike_abstracts_output_file.write(entity_abstract)

            finally:
                self.kb_abstracts_quantity = hudongbaike_abstracts_counter

                if hudongbaike_abstracts_file:
                    hudongbaike_abstracts_file.close()

                if hudongbaike_abstracts_output_file:
                    hudongbaike_abstracts_output_file.close()

        # zhwiki
        if self.kb_name == 'zhwiki':
            try:
                zhwiki_abstracts_file = open(self.kb_abstracts_path, 'r')
                zhwiki_abstracts_output_file = open(self.abstracts_output_path, 'a')
                zhwiki_abstracts_counter = 0
                zhwiki_abstracts_sum = 324627

                for line in zhwiki_abstracts_file.readlines():
                    zhwiki_abstracts_counter += 1
                    line = line.strip('\n')

                    # split
                    firstsplit = line.split('> <')
                    entity = firstsplit[0]

                    secondsplit = firstsplit[1].split('> "')
                    abstract = secondsplit[1]

                    # clean
                    entity = entity[1:]
                    entity = entity.replace('http://zhishi.me/zhwiki/resource/', '')
                    abstract = abstract[:-6]

                    # convert
                    entity = unquote(entity)

                    try:
                        abstract = eval("u'%s'" % (abstract)).encode('utf8')
                        entity_abstract = '<' + entity + '> <' + abstract + '>\n'

                    except:
                        entity_abstract = '<' + entity + '> <' + abstract + '>\n'

                    zhwiki_abstracts_output_file.write(entity_abstract)

            finally:
                self.kb_abstracts_quantity = zhwiki_abstracts_counter

                if zhwiki_abstracts_file:
                    zhwiki_abstracts_file.close()

                if zhwiki_abstracts_output_file:
                    zhwiki_abstracts_output_file.close()


    # 将实体和同义词合并
    def conbine_entity_synonym(self):
        # baidubaike
        if self.kb_name == 'baidubaike':
            try:
                baidubaike_entity_file = open(self.entity_url_output_path, 'r')
                baidubaike_synonym_file = open(self.synonym_path, 'r')
                baidubaike_entity_synonym_file = open(self.entity_synonym_output_path, 'a')
                baidubaike_synonym = []
                baidubaike_synonym_quantity = 77509
                synonym_counter = 0

                for line in baidubaike_synonym_file.readlines():
                    synonym_counter += 1
                    dict = {}
                    line = line.strip('\n')

                    # split
                    split1 = line.split('> <')
                    entity = split1[0]
                    split2 = split1[1].split('> [')
                    syn = split2[1]

                    # clean
                    entity = entity[1:]
                    syn = syn[:-2]

                    dict['entity'] = entity
                    dict['synonym'] = syn

                    baidubaike_synonym.append(dict)

                for line in baidubaike_entity_file.readlines():
                    line = line.strip('\n')

                    # split
                    split = line.split('> <')
                    entity = split[0]
                    url = split[1]

                    # clean
                    entity = entity[1:]
                    url = url[:-1]

                    # combine
                    synonym = ''

                    for d in baidubaike_synonym:
                        if entity == d['entity']:
                            synonym = d['synonym']
                            break

                    entity_synonym = '<' + entity + '> <' + synonym + '>\n'
                    baidubaike_entity_synonym_file.write(entity_synonym)

            finally:
                self.synonym_quantity = synonym_counter

                if baidubaike_entity_file:
                    baidubaike_entity_file.close()

                if baidubaike_synonym_file:
                    baidubaike_synonym_file.close()

                if baidubaike_entity_synonym_file:
                    baidubaike_entity_synonym_file.close()

        # hudongbaike
        if self.kb_name == 'hudongbaike':
            try:
                hudongbaike_entity_file = open(self.entity_url_output_path, 'r')
                hudongbaike_synonym_file = open(self.synonym_path, 'r')
                hudongbaike_entity_synonym_file = open(self.entity_synonym_output_path, 'a')
                hudongbaike_synonym = []
                hudongbaike_synonym_quantity = 37566
                synonym_counter = 0

                for line in hudongbaike_synonym_file.readlines():
                    synonym_counter += 1
                    dict = {}
                    line = line.strip('\n')

                    # split
                    split1 = line.split('> <')
                    entity = split1[0]
                    split2 = split1[1].split('> [')
                    syn = split2[1]

                    # clean
                    entity = entity[1:]
                    syn = syn[:-2]

                    dict['entity'] = entity
                    dict['synonym'] = syn

                    hudongbaike_synonym.append(dict)

                for line in hudongbaike_entity_file.readlines():
                    line = line.strip('\n')

                    # split
                    split = line.split('> <')
                    entity = split[0]
                    url = split[1]

                    # clean
                    entity = entity[1:]
                    url = url[:-1]

                    # combine
                    synonym = ''

                    for d in hudongbaike_synonym:
                        if entity == d['entity']:
                            synonym = d['synonym']
                            break

                    entity_synonym = '<' + entity + '> <' + synonym + '>\n'
                    hudongbaike_entity_synonym_file.write(entity_synonym)

            finally:
                self.synonym_quantity = synonym_counter

                if hudongbaike_entity_file:
                    hudongbaike_entity_file.close()

                if hudongbaike_synonym:
                    hudongbaike_synonym.close()

                if hudongbaike_entity_synonym_file:
                    hudongbaike_entity_synonym_file.close()

        # zhwiki
        if self.kb_name == 'zhwiki':
            try:
                zhwiki_entity_file = open(self.entity_url_output_path, 'r')
                zhwiki_synonym_file = open(self.synonym_path, 'r')
                zhwiki_entity_synonym_file = open(self.entity_synonym_output_path, 'a')
                zhwiki_synonym = []
                zhwiki_synonym_quantity = 443
                synonym_counter = 0

                for line in zhwiki_synonym_file.readlines():
                    synonym_counter += 1
                    dict = {}
                    line = line.strip('\n')

                    # split
                    split1 = line.split('> <')
                    entity = split1[0]
                    split2 = split1[1].split('> [')
                    syn = split2[1]

                    # clean
                    entity = entity[1:]
                    syn = syn[:-2]

                    dict['entity'] = entity
                    dict['synonym'] = syn

                    zhwiki_synonym.append(dict)

                for line in zhwiki_entity_file.readlines():
                    line = line.strip('\n')

                    # split
                    split = line.split('> <')
                    entity = split[0]
                    url = split[1]

                    # clean
                    entity = entity[1:]
                    url = url[:-1]

                    # combine
                    synonym = ''

                    for d in zhwiki_synonym:
                        if entity == d['entity']:
                            synonym = d['synonym']
                            break

                    entity_synonym = '<' + entity + '> <' + synonym + '>\n'
                    zhwiki_entity_synonym_file.write(entity_synonym)

            finally:
                self.synonym_quantity = synonym_counter

                if zhwiki_entity_file:
                    zhwiki_entity_file.close()

                if zhwiki_synonym_file:
                    zhwiki_synonym_file.close()

                if zhwiki_entity_synonym_file:
                    zhwiki_entity_synonym_file.close()


