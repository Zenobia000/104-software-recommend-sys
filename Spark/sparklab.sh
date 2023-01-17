#!/usr/bin/bash

export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="lab --no-browser --port=8888"

# lcoal mode
pyspark  --driver-memory 1G \
   --num-executors 100 \
   --driver-cores 3 \
   --executor-memory 6G \
   --executor-cores 4 \
   --total-executor-cores 999
   --conf spark.rpc.message.maxSize=2048	 

# standalone cluster
