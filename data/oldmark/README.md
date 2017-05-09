# MK-EL

This project aims to link string mentions in table cells to multiple linked knowledge bases. Here, we publish the benchmark of the sampled Web tables, where each string mention is linked to the entities in Zhishi.me, the largest Chinese LOD consisting of three Chinese linked KBs: Chinese Wikipedia, Baidu Baike and Hudong Baike.

## Naming Rule

* human_mark_kb_id
  * "name": In first row of each table, "name" means string in header cells. Otherwise, it means the name of referent entity in a KB.
  * "id": the id of entity in our database
* human_mark_kb_entity
  * "head": header cells string. For header cells in each table, we don't perform EL on them.
  * "mention": mention in non-header cells
  * "entity": mention's referent entity in a KB
* human_mark_kb_zhishime_url
  * "head": header cells string. For header cells in each table, we don't perform EL on them.
  * "mention": mention in non-header cells
  * "entity": mention's referent entity in a KB
  * "zhishime_url": the url of entity in [zhishi.me](http://zhishi.me)
* human_mark_kb_wiki_url
  * "head": header cells string. For header cells in each table, we don't perform EL on them.
  * "mention": mention in non-header cells
  * "entity": mention's referent entity in a KB
  * "zhwiki_url": the url of entity in [zhwiki](https://zh.wikipedia.org/wiki/Wikipedia:首页)


## Table

The "table" folder contains tables used for our experiments. The filename is like "table_123", in which 123 is the number of tables in this file.