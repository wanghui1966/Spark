import os
import shutil
import pandas as pd
from pyspark.sql import SparkSession

def calc_func(data):
	result = []
	if data % 2 == 0:
		result.append(data * 10)
	else:
		result.append(data * 100)
	return result

if __name__ == "__main__":
	spark = SparkSession.builder.appName("spark_explame").master("local[*]").getOrCreate()

	executor_cores = int(spark.sparkContext.getConf().get("spark.executor.cores", '2'))
	num_executors = int(spark.sparkContext.getConf().get("spark.executor.instances", '2'))
	par_num = executor_cores * num_executors
	print("executor_cores={}, num_executors={}, par_num={}".format(executor_cores, num_executors, par_num))

	data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	print("data={}".format(data))
	rdd_data = spark.sparkContext.parallelize(data, par_num)

	result = rdd_data.map(calc_func).reduce(lambda a, b: a + b)
	print("result={}".format(result))
	if os.path.exists("output"):
		shutil.rmtree("output")
	spark.sparkContext.parallelize(result).repartition(1).saveAsTextFile("file:///home/huiwang/project/Spark/output")
