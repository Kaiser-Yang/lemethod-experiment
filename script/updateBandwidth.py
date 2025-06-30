#!/usr/bin/env python3

# Usage: python3 updateBandwidth.py <projectName> [changable]

# NOTE: when changable is 1, the default value is 0, every link's
#       bandwidth will change randomly in random time, so you need to
#       close the process mannully.

# bandwidth will be generated with norm distribution,
# the variables below are to control the mean and std.
# the unit is Kbps

from vemu_api import LinkConfiguration
import random
from commonConfig import init
import commonConfig
import time
import sys
import os
import time
import traceback

# unit: kbps
bandwidthMinValue = int(80 * 8 * 1e3)
bandwidthMaxValue = int(240 * 8 * 1e3)

# every link's bandwidth will change in some seconds,
# the unit is second(s)
updateTimeMinValue = 1 * 60
updateTimeMaxValue = 5 * 60

bandwidthFile = None
logFile = None


def currentTime() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def updateLinkConfig(linkName, newBandwidth, linkMap):
    global logFile
    assert(logFile != None)
    srcLinkConfig = LinkConfiguration(link=linkName,
                                      ne=linkMap[linkName].source,
                                      queue_size_bytes="1100000000",
                                      bw_kbps=newBandwidth)
    destLinkConfig = LinkConfiguration(link=linkName,
                                       ne=linkMap[linkName].target,
                                       queue_size_bytes="1100000000",
                                       bw_kbps=newBandwidth)
    while True:
        try:
            # update config
            commonConfig.linkManager.config_link(srcLinkConfig, destLinkConfig)
            logFile.write(f"{currentTime()} configure linkage ({linkName}) between "
                          f"{linkMap[linkName].source} and {linkMap[linkName].target}: "
                          f"{newBandwidth} kbps\n")
        except Exception:
            bt = traceback.format_exc()
            logFile.write(bt)
            logFile.write('\n')
            logFile.write('exception catched, retry after 5 seconds\n')
            time.sleep(5)
        else:
            break
        finally:
            logFile.flush()


def getBandwidth(newBandwidth, updateTime, linkNum):
    global bandwidthFile
    assert(bandwidthFile != None)
    line = bandwidthFile.readline()
    # file has contents, use the contents
    if line:
        word = line.split()
        if len(word) == 2 * linkNum:
            for i in range(linkNum):
                newBandwidth.append(word[2 * i])
                updateTime.append(int(word[2 * i + 1]))
            return

    for i in range(linkNum):
        newBandwidth.append(random.randint(bandwidthMinValue, bandwidthMaxValue))
        newBandwidth[i] = str(newBandwidth[i])
    for i in range(linkNum):
        updateTime.append(random.randint(updateTimeMinValue, updateTimeMaxValue))
    for i in range(linkNum):
        bandwidthFile.write(f'{newBandwidth[i]} {updateTime[i]}')
        if i != linkNum - 1:
            bandwidthFile.write(' ')
        else:
            bandwidthFile.write('\n')
    bandwidthFile.flush()
    # move cursor to the end of the file
    bandwidthFile.seek(0, 2)


def updateBandwidthOnce(instant, linkNum, linkMap):
    global logFile
    assert(logFile != None)
    newBandwidth = []
    updateTime = []
    getBandwidth(newBandwidth, updateTime, linkNum)
    logFile.writelines([f'{currentTime()} newBandwidth: {newBandwidth}\n'])
    logFile.flush()
    if instant:
        for i, linkName in zip(range(linkNum), linkMap):
            updateLinkConfig(linkName, newBandwidth[i], linkMap)
        return
    INF = 2 ** 31 - 1
    while True:
        minUpdateTime = min(updateTime)
        logFile.writelines([f'{currentTime()} updateTime: {updateTime}\n',
                            f'{currentTime()} minUpdateTime: {minUpdateTime}\n'])
        logFile.flush()
        if minUpdateTime == INF:
            break
        time.sleep(minUpdateTime)
        for i, linkName in zip(range(linkNum), linkMap):
            if updateTime[i] == INF:
                continue
            updateTime[i] -= minUpdateTime
            if updateTime[i] != 0:
                continue
            updateTime[i] = INF
            updateLinkConfig(linkName, newBandwidth[i], linkMap)


def updateBandwidth(projectName: str, changable: bool = False) -> int:
    global bandwidthFile, logFile
    init(projectName)
    if projectName not in commonConfig.projectManager.get_projects():
        print(f"There is no project {projectName}, so check you project name.")
        return 1
    linkMap = commonConfig.linkManager.get_links()
    linkNum = len(linkMap)
    fileName = f'bandwidth/bandwidth_{projectName}_{linkNum}.txt'
    logFileName = f'bandwidth/bandwidth_{projectName}_{linkNum}.log'
    if not os.path.exists('bandwidth'):
        os.mkdir('bandwidth')
    if not os.path.exists(fileName):
        os.mknod(fileName)
    bandwidthFile = open(fileName, 'r+')
    logFile = open(logFileName, 'w')
    if changable == 0:
        updateBandwidthOnce(True, linkNum, linkMap)
        bandwidthFile.close()
        logFile.close()
        return 0
    cnt = 0
    while True:
        cnt += 1
        logFile.write(f'cnt: {cnt}\n')
        updateBandwidthOnce(False, linkNum, linkMap)


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2 or argc > 3:
        print("python3 updateBandwidth.py <projectName> [changable]")
        exit(1)
    projectName = sys.argv[1]
    if argc == 3:
        changable = bool(int(sys.argv[2]))
    else:
        changable = False
    if changable:
        print("set changable be 1. Remember kill the process mannully.")
    exit(updateBandwidth(projectName, changable))
