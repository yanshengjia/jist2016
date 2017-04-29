# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn
# 实验的第四步：利用多知识库间sameAs关系提升链接质量

from urllib import unquote


class SameAs(object):
    # table_name: 表格文件的名称
    # table_path: 表格文件的路径
    # output_path: 生成好的候选实体的输出路径
    def __init__(self, table_name, table_path, output_path):
        self.table_name = table_name
        self.table_path = table_path
        self.output_path = output_path

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

    # 挑选每个 mention 的候选实体概率排名列表中的前3个
    def sameAs(self):
        print

