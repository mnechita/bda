import os
from itertools import chain

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages graphframes:graphframes:0.5.0-spark2.1-s_2.11'

from pyspark.shell import spark, sc
import pyspark.sql.functions as F
import pyspark

df = spark.read.json('small_sample/')
df.printSchema()

auts = df.select('front.article_meta.authors.surname').rdd.flatMap(lambda xs: chain(*xs)).distinct()
