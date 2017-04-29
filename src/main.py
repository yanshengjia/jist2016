# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 总控程序

from preprocess import *
from candidate import *
from disambiguation import *
from sameas import *


# Step 1: 原始数据预处理
def preprocess():
    # baidubaike
    kb_name = 'baidubaike'
    kb_labels_path = '../../../data/raw/kb_labels/3.0_baidubaike_labels_zh.nt'
    entity_url_output_path = '../../../data/entity/baidubaike_entity_url.txt'
    kb_infobox_properties_path = '../../../data/raw/kb_infobox_properties/3.0_baidubaike_infobox_properties_zh.nt'
    infobox_properties_output_path = '../../../data/property/baidubaike_infobox_properties.txt'
    kb_abstracts_path = '../../../data/raw/kb_abstracts/3.0_baidubaike_abstracts_zh.nt'
    abstracts_output_path = '../../../data/abstract/baidubaike_abstracts.txt'
    synonym_path = '../../../data/synonym/baidubaike_entities_syn.txt'
    entity_synonym_output_path = '../../../data/entity/baidubaike_entity_synonym.txt'

    extracter_baidubaike = Preprocess(kb_name, kb_labels_path, entity_url_output_path, kb_infobox_properties_path, infobox_properties_output_path, kb_abstracts_path, abstracts_output_path, synonym_path, entity_synonym_output_path)

    # print 'Extracting entities from ' + kb_name + ' labels......',
    # extracter_baidubaike.extract_entity()
    # print 'Done!'
    #
    # print 'Extracting infobox properties from ' + kb_name + ' infobox properties......',
    # extracter_baidubaike.extract_infobox_properties()
    # print 'Done!'
    #
    # print 'Extracting abstracts from ' + kb_name + ' abstracts......',
    # extracter_baidubaike.extract_abstracts()
    # print 'Done!'

    print 'Conbining entities and synonyms of ' + kb_name + '......',
    extracter_baidubaike.conbine_entity_synonym()
    print 'Done!'


    # hudongbaike
    kb_name = 'hudongbaike'
    kb_labels_path = '../../../data/raw/kb_labels/3.0_hudongbaike_labels_zh.nt'
    entity_url_output_path = '../../../data/entity/hudongbaike_entity_url.txt'
    kb_infobox_properties_path = '../../../data/raw/kb_infobox_properties/3.0_hudongbaike_infobox_properties_zh.nt'
    infobox_properties_output_path = '../../../data/property/hudongbaike_infobox_properties.txt'
    kb_abstracts_path = '../../../data/raw/kb_abstracts/3.0_hudongbaike_abstracts_zh.nt'
    abstracts_output_path = '../../../data/abstract/hudongbaike_abstracts.txt'
    synonym_path = '../../../data/synonym/hudongbaike_entities_syn.txt'
    entity_synonym_output_path = '../../../data/entity/hudongbaike_entity_synonym.txt'

    extracter_hudongbaike = Preprocess(kb_name, kb_labels_path, entity_url_output_path, kb_infobox_properties_path, infobox_properties_output_path, kb_abstracts_path, abstracts_output_path, synonym_path, entity_synonym_output_path)

    # print 'Extracting entities from ' + kb_name + ' labels......',
    # extracter_hudongbaike.extract_entity()
    # print 'Done!'
    #
    # print 'Extracting infobox properties from ' + kb_name + ' infobox properties......',
    # extracter_hudongbaike.extract_infobox_properties()
    # print 'Done!'
    #
    # print 'Extracting abstracts from ' + kb_name + ' abstracts......',
    # extracter_hudongbaike.extract_abstracts()
    # print 'Done!'

    print 'Conbining entities and synonyms of ' + kb_name + '......',
    extracter_hudongbaike.conbine_entity_synonym()
    print 'Done!'

    # zhwiki
    kb_name = 'zhwiki'
    kb_labels_path = '../../../data/raw/kb_labels/3.1_zhwiki_labels_zh.nt'
    entity_url_output_path = '../../../data/entity/zhwiki_entity_url.txt'
    kb_infobox_properties_path = '../../../data/raw/kb_infobox_properties/2.0_zhwiki_infobox_properties_zh.nt'
    infobox_properties_output_path = '../../../data/property/zhwiki_infobox_properties.txt'
    kb_abstracts_path = '../../../data/raw/kb_abstracts/2.0_zhwiki_abstracts_zh.nt'
    abstracts_output_path = '../../../data/abstract/zhwiki_abstracts.txt'
    synonym_path = '../../../data/synonym/zhwiki_entities_syn.txt'
    entity_synonym_output_path = '../../../data/entity/zhwiki_entity_synonym.txt'

    extracter_zhwiki = Preprocess(kb_name, kb_labels_path, entity_url_output_path, kb_infobox_properties_path, infobox_properties_output_path, kb_abstracts_path, abstracts_output_path, synonym_path, entity_synonym_output_path)

    # print 'Extracting entities from ' + kb_name + ' labels......',
    # extracter_zhwiki.extract_entity()
    # print 'Done!'
    #
    # print 'Extracting infobox properties from ' + kb_name + ' infobox properties......',
    # extracter_zhwiki.extract_infobox_properties()
    # print 'Done!'
    #
    # print 'Extracting abstracts from ' + kb_name + ' abstracts......',
    # extracter_zhwiki.extract_abstracts()
    # print 'Done!'

    print 'Conbining entities and synonyms of ' + kb_name + '......',
    extracter_zhwiki.conbine_entity_synonym()
    print 'Done!'


# Step 2: 候选实体生成
def candidate_generation():
    # baidubaike
    table_name = 'table_123'
    table_path = '../../../data/table/table_123.xls'
    kb_name = 'baidubaike'
    entity_path = '../../../data/entity/baidubaike_entity_synonym.txt'
    candidate_path = '../../../data/candidate/baidubaike_candidate_entities.txt'

    baidubaike_candidate_generater = Candidate(table_name, table_path, kb_name, entity_path, candidate_path)

    print 'Generating candidate entities for mentions based on ' + kb_name + '......',
    baidubaike_candidate_generater.generate_candidate()
    print 'Done!'


    # hudongbaike
    table_name = 'table_123'
    table_path = '../../../data/table/table_123.xls'
    kb_name = 'hudongbaike'
    entity_path = '../../../data/entity/hudongbaike_entity_synonym.txt'
    candidate_path = '../../../data/candidate/hudongbaike_candidate_entities.txt'

    hudongbaike_candidate_generater = Candidate(table_name, table_path, kb_name, entity_path, candidate_path)

    print 'Generating candidate entities for mentions based on ' + kb_name + '......',
    hudongbaike_candidate_generater.generate_candidate()
    print 'Done!'


    # zhwiki
    table_name = 'table_123'
    table_path = '../../../data/table/table_123.xls'
    kb_name = 'zhwiki'
    entity_path = '../../../data/entity/zhwiki_entity_synonym.txt'
    candidate_path = '../../../data/candidate/zhwiki_candidate_entities.txt'

    zhwiki_candidate_generater = Candidate(table_name, table_path, kb_name, entity_path, candidate_path)

    print 'Generating candidate entities for mentions based on ' + kb_name + '......',
    zhwiki_candidate_generater.generate_candidate()
    print 'Done!'


# Step 3: 实体消岐
def entity_disambiguation():
    # baidubaike
    table_name = 'table_123'
    table_path = '../../../data/table/table_123.xls'
    kb_name = 'baidubaike'
    candidate_name = 'baidubaike_candidate_entities'
    candidate_path = '../../../data/candidate/baidubaike_candidate_entities.txt'
    graph_path = '../../../data/disambiguation/baidubaike/graph/'
    disambiguation_output_path = '../../../data/disambiguation/baidubaike/result/'
    infobox_property_path = '../../../data/property/baidubaike_infobox_properties.txt'

    baidubaike_judger = Disambiguation(table_name, table_path, kb_name, candidate_name, candidate_path, graph_path, disambiguation_output_path, infobox_property_path)

    print 'Disambiguating candidate entities based on ' + kb_name + ':'
    baidubaike_judger.disambiguation()


    # hudongbaike
    table_name = 'table_123'
    table_path = '../../../data/table/table_123.xls'
    kb_name = 'hudongbaike'
    candidate_name = 'hudongbaike_candidate_entities'
    candidate_path = '../../../data/candidate/hudongbaike_candidate_entities.txt'
    graph_path = '../../../data/disambiguation/hudongbaike/graph/'
    disambiguation_output_path = '../../../data/disambiguation/hudongbaike/result/'
    infobox_property_path = '../../../data/property/hudongbaike_infobox_properties.txt'

    hudongbaike_judger = Disambiguation(table_name, table_path, kb_name, candidate_name, candidate_path, graph_path, disambiguation_output_path, infobox_property_path)

    print 'Disambiguating candidate entities based on ' + kb_name + ':'
    hudongbaike_judger.disambiguation()


    # zhwiki
    table_name = 'table_123'
    table_path = '../../../data/table/table_123.xls'
    kb_name = 'zhwiki'
    candidate_name = 'zhwiki_candidate_entities'
    candidate_path = '../../../data/candidate/zhwiki_candidate_entities.txt'
    graph_path = '../../../data/disambiguation/zhwiki/graph/'
    disambiguation_output_path = '../../../data/disambiguation/zhwiki/result/'
    infobox_property_path = '../../../data/property/zhwiki_infobox_properties.txt'

    zhwiki_judger = Disambiguation(table_name, table_path, kb_name, candidate_name, candidate_path, graph_path, disambiguation_output_path, infobox_property_path)

    print 'Disambiguating candidate entities based on ' + kb_name + ':'
    zhwiki_judger.disambiguation()


# Step 4: 利用多知识库间sameAs关系提升链接质量
def sameAs():
    print 'Improving entity linking with multiple linked KBs......',

    multiple_kb_improver = SameAs()
    multiple_kb_improver.sameAs()

    print 'Done!'


def main():
    print "Entity Linking System in Web Tables with Multiple Linked Knowledge Bases"
    print "Version 1.0"
    print "Copyright @2017/3/1 Shengjia Yan. All Rights Reserved."

    preprocess()
    # candidate_generation()
    # entity_disambiguation()
    # sameAs()

if __name__ == "__main__":
    main()
