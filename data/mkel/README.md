# MK-EL
This project aims to link string mentions in table cells to multiple linked knowledge bases. Here, we publish the benchmark of the sampled Web tables, where each string mention is linked to the entities in Zhishi.me, the largest Chinese LOD consisting of three Chinese linked KBs: Chinese Wikipedia, Baidu Baike and Hudong Baike.

***

**Naming Rule:**

* human_mark_kb_id: {“id”: entity id in our database, "name": mention name}
* human_mark_kb_url: {“id”: entity url in zhishi.me, "name": mention name}
* human_mark_kb_wikiurl: {“id”: entity url in zhwikipedia, "name": mention name}