#!/usr/bin/env python3

# Usage: python3 experiment.py WORKER_NUM MODULE_SIZE ITERATION SLEEP_AFTER_PULL

import mxnet
import sys
import time
import os
import random

def getSleepTime() -> int:
    if sleepAfterPull == 0:
        return 0
    global calculationTimeFile
    assert(calculationTimeFile != None)
    sleepTime = calculationTimeFile.readline()

    # file has content, use the content
    if sleepTime:
        return int(sleepTime)

    # random sleep time between [0, 10]
    sleepTime = random.randint(0, 10)
    calculationTimeFile.write(f'{sleepTime}\n')
    calculationTimeFile.flush()
    # move cursor to the end of the file
    calculationTimeFile.seek(0, 2)
    return sleepTime

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 5:
        print('Usage: python3 experiment.py WORKER_NUM MODULE_SIZE ITERATION SLEEP_AFTER_PULL')
        exit(1)
    else:
        workerNum = int(sys.argv[1])
        moduleSize = int(sys.argv[2])
        iteration = int(sys.argv[3])
        sleepAfterPull = int(sys.argv[4])

    if sleepAfterPull == 1:
        if not os.path.exists('/root/calculationTimeFile.txt'):
            os.mknod('/root/calculationTimeFile.txt')
        calculationTimeFile = open('/root/calculationTimeFile.txt', 'r+')

    parameterNum = int(moduleSize * 1024 * 1024 / 4)
    kvstore = mxnet.kv.create('dist_sync')

    experimentLogFile = open('/root/experimentLog.log', 'w')
    experimentLogFile.write(f'parameterNum: {parameterNum}\n')
    experimentLogFile.write(f'start init at: {time.time()}\n')
    shape = (parameterNum)
    kvstore.init(0, mxnet.nd.ones(shape))
    a = mxnet.nd.ones(shape)
    kvstore.pull(0, out = a)
    experimentLogFile.write(f'after pull at {time.time()}\n')
    experimentLogFile.flush()
    # for will be extremely time-consuming,
    # maybe the iterator is O(n),
    # so we use print to make sure the data is ready.
    experimentLogFile.write(f'{a}\n')
    experimentLogFile.write(f'finish init at: {time.time()}\n')
    experimentLogFile.flush()
    outputFile = open('/root/experimentResult.out', 'w')
    for i in range(iteration):
        outputFile.write(f'{time.time()}')
        outputFile.flush()
        kvstore.push(0, mxnet.nd.ones(shape))
        kvstore.pull(0, out = a)
        experimentLogFile.write(f'{a}\n')
        experimentLogFile.flush()
        outputFile.write(f' {time.time()}\n')
        outputFile.flush()
        sleepTime = getSleepTime()
        if sleepTime > 0:
            time.sleep(sleepTime)
    outputFile.close()
    experimentLogFile.close()
