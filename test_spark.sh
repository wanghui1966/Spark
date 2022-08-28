
spark-submit \
--master local[*] \
--deploy-mode client \
--driver-memory 1G \
--executor-cores 2 \
--num-executors 2 \
spark_example.py 1> log.log 2>&1
