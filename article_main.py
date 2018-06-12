import itertools
import os
from itertools import chain

from pyspark import SparkContext, SQLContext

from article import Article
from graphframes import *
from graphframes.python.graphframes import GraphFrame

sc = SparkContext()
sqlCtx = SQLContext(sc)

df = sqlCtx.read.json('small_sample/')
df.printSchema()

# auts = df.select('front.article_meta.authors.surname').rdd.flatMap(lambda xs: chain(*xs)).distinct()
#
# articles = df.select('front.article_meta.article_title', 'front.article_meta.article_ids',
#                      'back.ref_list.referred_article_ids').map(lambda x: Article(x))
#
# ref_articles = df.select('back.ref_list[i].referred_article_ids', 'back.ref_list[i].article_title').rdd
#
# print(ref_articles.collect()[0])
# all_articles = articles.join(ref_articles, on = "ids")

# a1 = articles.collect()[0]
# a2 = articles.collect()[1]
#
# print(a1)
# print(a2)
# print()


# gr = GraphFrame(articles, citations)
#
# gr.inDegrees().show()

#
# i = 1
#
# processed_articles = {articles.collect()[0]: i}
#
# for a in articles.collect()[1:]:
#     # if a not in processed_articles:
#     #     i += 1
#     #     a.uniq_id = i
#     #     processed_articles[a] = i
#     # else:
#     #     a.uniq_id = processed_articles[a]
#
#     i += 1
#
#     ok = False
#     obj = []
#     for pa in processed_articles.items():
#         if a == pa[0]:
#             obj = [a, pa[1]]
#             ok = True
#             break
#
#     if not ok:
#         obj = [a, i]
#
#     processed_articles[obj[0]] = obj[1]
#
#
# articles = articles.map(lambda a: a.set_id(processed_articles[a]))
# articles = articles.map(lambda a: )
# print(articles.collect())
# citations = articles.map(lambda x: tuple(zip(itertools.repeat(x.uniq_id), x.ref_list)))
#
# print(citations.collect())