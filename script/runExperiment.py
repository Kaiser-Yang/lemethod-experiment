#!/usr/bin/env python3

# Usage: python runExperiment.py PROJECT_NAME LEMETHOD|TSENGINE|DEFAULT
#        CONNECTION_TYPE SCHEDULE_NUM MODULE_SIZE ITERATION GREED_RATE
#        VERBOSE

import sys
import commonConfig
from commonConfig import execCmd
from commonConfig import getWorkerName
import os


def updateConfigFile() -> None:
    expiration = 5 if SLEEP_AFTER_PULL else 999999
    execCmd("server", f'bash -c "echo \'SET_SCHEDULE_NUM {scheduleNum}\' >> /root/lemethod.conf"')
    execCmd("server", f'bash -c "echo \'SET_BANDWIDTH_EXPIRATION {expiration}\' >> /root/lemethod.conf"')
    execCmd("server", f'bash -c "echo \'SET_MAX_RECEIVING_LIMIT 5\' >> /root/lemethod.conf"')
    for i in range(workerNum):
        execCmd(getWorkerName(i),
                f'bash -c "echo \'SET_SCHEDULE_NUM {scheduleNum}\' >> /root/lemethod.conf"')
        execCmd(getWorkerName(i),
                f'bash -c "echo \'SET_BANDWIDTH_EXPIRATION {expiration}\' >> /root/lemethod.conf"')
        execCmd(getWorkerName(i),
                f'bash -c "echo \'SET_MAX_RECEIVING_LIMIT 5\' >> /root/lemethod.conf"')


def startExperiment(projectName) -> None:
    os.system(f"bash -c 'nohup ./updateBandwidth.py {projectName} 1 &'")
    args = f'{workerNum} {enableLeMethod} {enableTSEngine} {connectionType} {greedRate} {VERBOSE}'
    execCmd("server", f'bash -c "cd /root && nohup bash /root/start_scheduler.sh {args}"')
    execCmd("server", f'bash -c "cd /root && nohup bash /root/start_server.sh {args}"')
    for i in range(workerNum):
        # this workerIP is important,
        # mxnet may get the wrong ip on this platform
        # so you need specify the ip manually
        workerIP = commonConfig.getIP("192.168.0.0", i + 1).split('/')[0]
        workerArgs = args + f" {i} {modeuleSize} {iteration} {workerIP} {SLEEP_AFTER_PULL}"
        execCmd(getWorkerName(i),
                f'bash -c "cd /root && nohup bash /root/start_worker.sh {workerArgs}"')


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 8:
        print("Usage: python runExperiment.py PROJECT_NAME LEMETHOD|TSENGINE|DEFAULT "
              "CONNECTION_TYPE SCHEDULE_NUM MODULE_SIZE ITERATION GREED_RATE [VERBOSE] "
              "[SLEEP_AFTER_PULL]")
        exit(1)
    else:
        projectName = sys.argv[1]
        enableTSEngine = 0
        enableLeMethod = 0
        if sys.argv[2] == "LEMETHOD":
            enableLeMethod = 1
        elif sys.argv[2] == "TSENGINE":
            enableTSEngine = 1
        elif sys.argv[2] != "DEFAULT":
            print("unknown parameter, must be in [LEMETHOD|TSENGINE|DEFAULT]")
            exit(1)
        connectionType = int(sys.argv[3])
        scheduleNum = int(sys.argv[4])
        modeuleSize = int(sys.argv[5])
        iteration = int(sys.argv[6])
        greedRate = float(sys.argv[7])
        if argc > 8:
            VERBOSE = int(sys.argv[8])
        else:
            VERBOSE = 0
        if argc > 9:
            SLEEP_AFTER_PULL = int(sys.argv[9])
        else:
            SLEEP_AFTER_PULL = 0
    commonConfig.init(projectName)
    workerNum = 0
    for nodeName in commonConfig.nodeManager.get_nodes():
        if "worker" in nodeName:
            workerNum += 1
    if enableLeMethod == 1:
        updateConfigFile()
    startExperiment(projectName)
