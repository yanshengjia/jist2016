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
    def __init__(self, kb_name, kb_labels_path, entity_url_output_path, kb_infobox_properties_path, infobox_properties_output_path):
        self.kb_name = kb_name
        self.kb_labels_path = kb_labels_path
        self.entity_url_output_path = entity_url_output_path
        self.kb_entity_quantity = 0
        self.kb_infobox_properties_path = kb_infobox_properties_path
        self.infobox_properties_output_path = infobox_properties_output_path
        self.kb_infobox_properties_quantity = 0
        self.kb_infobox_property_definitions_quantity = 0

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
                    baidubaike_entity_counter += 1
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
                # print 'baidubaike entity counter: ' + str(baidubaike_entity_counter)
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
                # print 'hudongbaike entity counter: ' + str(hudongbaike_entity_counter)
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
                # print 'zhwiki entity counter: ' + str(zhwiki_entity_counter)
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
                # print 'zhwiki infobox properties counter: ' + str(baidubaike_infobox_properties_counter)
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
                print 'zhwiki infobox properties counter: ' + str(hudongbaike_infobox_properties_counter)
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
                # print 'zhwiki infobox properties counter: ' + str(zhwiki_infobox_properties_counter)
                self.kb_infobox_properties_quantity = zhwiki_infobox_properties_counter

                if zhwiki_infobox_properties:
                    zhwiki_infobox_properties.close()

                if zhwiki_isrdf:
                    zhwiki_isrdf.close()

