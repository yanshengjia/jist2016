# !/usr/bin/python
# coding=utf8
# Created by sjyan @2017-03-06


from urllib import quote
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

list = open('./list_mkel.txt', 'r') # list0: baidubaike, list1: hudongbaike, list2: zhwiki
list_counter = 0


for route in list.readlines():
    route = route.strip('\n')
    infile = open(route, 'r').read()

    if list_counter == 0:
        preurl = "http://zhishi.me/baidubaike/resource/"
    if list_counter == 1:
        preurl = "http://zhishi.me/hudongbaike/resource/"
    if list_counter == 2:
        preurl = "http://zhishi.me/zhwiki/resource/"

    tables_json = json.loads(infile, encoding='utf8')

    # i: table number
    # j: row number
    # k: column number
    for i in range(0, len(tables_json)):
        for j in range(0, len(tables_json[i])):
            for k in range(0, len(tables_json[i][j])):
                if tables_json[i][j][k].has_key('name'):
                    if j == 0:
                            tables_json[i][j][k]["id"] = "Null"
                    else:
                        name = tables_json[i][j][k]["name"]
                        suffix = quote(name.encode('utf8'))
                        url = preurl + suffix
                        tables_json[i][j][k]["id"] = url

    tables_str = json.dumps(tables_json, ensure_ascii=False)

    if list_counter == 0:
        outfile = open("../../data/mkel/baidubaike/human_mark_baidubaike_url.txt", "w")
        outfile.write(tables_str)
    if list_counter == 1:
        outfile = open("../../data/mkel/hudongbaike/human_mark_hudongbaike_url.txt", "w")
        outfile.write(tables_str)
    if list_counter == 2:
        outfile = open("../../data/mkel/zhwiki/human_mark_zhwiki_url.txt", "w")
        outfile.write(tables_str)

        # convert entity url to zhwiki url
        preurl = "https://zh.wikipedia.org/wiki/"

        for i in range(0, len(tables_json)):
            for j in range(0, len(tables_json[i])):
                for k in range(0, len(tables_json[i][j])):
                    if tables_json[i][j][k].has_key('name'):
                        name = tables_json[i][j][k]["name"]
                        name = name.replace("["," (")
                        name = name.replace("]",")")
                        tables_json[i][j][k]["name"] = name
                        suffix = name
                        url = preurl + suffix
                        url = url.replace(" ","_")
                        tables_json[i][j][k]["id"] = url
                        
                        if j == 0:
                            tables_json[i][j][k]["id"] = "Null"
                            
        tables_str = json.dumps(tables_json, ensure_ascii=False)
        outfile_wiki = open("../../data/mkel/zhwiki/human_mark_zhwiki_wikiurl.txt", "w")
        outfile_wiki.write(tables_str)

    list_counter += 1

outfile.close()
outfile_wiki.close()
