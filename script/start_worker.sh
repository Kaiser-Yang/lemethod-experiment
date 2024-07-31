#!/bin/bash

# Uusage: bash start_worker.sh NUM_WORKER ENABLE_LEMETHOD ENABLE_TSENGINE LEMETHOD_CONNECTION_TYPE
#         GREED_RATE PS_VERBOSE DMLC_RNAK MODULE_SIZE ITERATION DMLC_NODE_HOST SLEEP_AFTER_PULL

NUM_WORKER=$1
ENABLE_LEMETHOD=$2
ENABLE_TSENGINE=$3
LEMETHOD_CONNECTION_TYPE=$4
# TSENGINE must with the GREED_RATE, because its codes do not check the environment variable.
GREED_RATE=$5
PS_VERBOSE=$6
DMLC_RNAK=$7
MODULE_SIZE=$8
ITERATION=$9
DMLC_NODE_HOST=${10}
SLEEP_AFTER_PULL=${11}

SCHEDULER_PORT=9092
WORKER_PATH='./experiment.py'
SCHEDULER_ADDRESS='192.168.0.1'

# start worker_$DML_RANK
export START_WORKER='/root/miniconda3/envs/lemethod/bin/python '$WORKER_PATH
DMLC_ROLE=worker \
DMLC_PS_ROOT_URI=$SCHEDULER_ADDRESS \
DMLC_PS_ROOT_PORT=$SCHEDULER_PORT \
DMLC_NUM_SERVER=1 \
DMLC_NUM_WORKER=$NUM_WORKER \
ENABLE_LEMETHOD=$ENABLE_LEMETHOD \
ENABLE_TSENGINE=$ENABLE_TSENGINE \
GREED_RATE=$GREED_RATE \
LEMETHOD_CONNECTION_TYPE=$LEMETHOD_CONNECTION_TYPE \
DMLC_RANK=$DMLC_RNAK \
PS_VERBOSE=$PS_VERBOSE \
DMLC_NODE_HOST=$DMLC_NODE_HOST \
$START_WORKER "$NUM_WORKER" "$MODULE_SIZE" "$ITERATION" "$SLEEP_AFTER_PULL" >> worker_"$DMLC_RNAK".log 2>&1 &
