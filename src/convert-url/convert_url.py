# !/usr/bin/python
# coding=utf8
# Created by sjyan @2017-03-06


from urllib import quote
import json

list = open('./list_mkel.txt', 'r') # list0: baidubaike, list1: hudongbaike, list2: zhwiki
list_counter = 0


for route in list.readlines():
    route = route.strip('\n')
    file = open(route, 'r').read()

    if list_counter == 0:
        preurl = "http://zhishi.me/baidubaike/resource/"
    if list_counter == 1:
        preurl = "http://zhishi.me/hudongbaike/resource/"
    if list_counter == 2:
        preurl = "http://zhishi.me/zhwiki/resource/"    

    tables = json.loads(file, encoding='utf8')

    for i in range(0, len(tables)):
        print "Table " + str(i) + ":"
        for j in range(0, len(tables[i])):
            for k in range(0, len(tables[i][j])):
                if tables[i][j][k].has_key('name'):
                    name = tables[i][j][k]["name"]
                    url = quote(name.encode('utf8'))
                    tables[i][j][k]["id"] = url
                    id = tables[i][j][k]["id"]
                    print "id: " + preurl + id + ", name: " + name
        print "\n"

    break
    list_counter += 1

