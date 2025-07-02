#!/usr/bin/env python3

# Usage: python createAdditionalLinkageTopo.py WOKER_NUM
#        [ADDTIONAL_LINKAGE_NUM]

import sys

import vemu_api
import commonConfig
from commonConfig import createServerAndWorker, createSwitchNode
from random import random
from prepareExperiment import prepareExperiment
from updateBandwidth import updateBandwidth


def generateConfigFile(contentList: list):
    assert (workerNum != None)
    content = ""
    for line in contentList:
        content += line + "\n"
    content = content[:-1]
    for i in range(workerNum):
        commonConfig.execCmd(commonConfig.getWorkerName(i),
                             f'bash -c "echo \'{content}\' > /root/lemethod.conf"')
    commonConfig.execCmd("server", f'bash -c "echo \'{content}\' > /root/lemethod.conf"')


def getAdditionalLinkageRandomly():
    assert (workerNum != None)
    unconnectedWorkerPair = []
    for i in range(workerNum):
        for j in range(i + 1, workerNum):
            unconnectedWorkerPair.append((i, j))
    configList = []
    for i in range(addtionalLinkageNum):
        pos = int(random() * len(unconnectedWorkerPair))
        i, j = unconnectedWorkerPair[pos]
        unconnectedWorkerPair.pop(pos)
        configList.append("ADD_CONNECTION " + str(i) + " " + str(j))
        configList.append("ADD_CONNECTION " + str(j) + " " + str(i))
    return configList


class UFS(object):
    def __init__(self, n):
        self.h = [0] * n
        self.n = n
        self.member = [set() for _ in range(n)]
        for i in range(n):
            self.h[i] = i
            self.member[i].add(i)

    def find(self, x) -> int:
        if x == self.h[x]:
            return x
        else:
            self.h[x] = self.find(self.h[x])
            return self.h[x]

    def same(self, a, b) -> bool:
        return self.find(a) == self.find(b)

    def join(self, a, b):
        fa, fb = self.find(a), self.find(b)
        self.h[fa] = fb
        self.member[fb] = self.member[fa] = self.member[fa].union(self.member[fb])

    def count(self, fa) -> int:
        return len(self.member[fa])

    def isFather(self, i) -> bool:
        return self.h[i] == i


def createAdditionalLinkageTopo() -> None:
    assert (workerNum != None)
    additionalLinkageTopo = vemu_api.Topo()

    serverAndWorkerMap = createServerAndWorker(additionalLinkageTopo,
                                               commonConfig.imageMap['lemethod'],
                                               workerNum)

    configList = getAdditionalLinkageRandomly()
    ufs = UFS(workerNum)
    for connection in configList:
        nodeID = connection.split(' ')[1:]
        ufs.join(int(nodeID[0]), int(nodeID[1]))

    switchNum = 0
    for i in range(workerNum):
        if ufs.isFather(i) and ufs.count(i) >= 2:
            switchNum += 1
            print(ufs.member[i])
    switchAndRouterMap = createSwitchNode(additionalLinkageTopo,
                                          commonConfig.imageMap['ovs'],
                                          switchNum)
    add_node = additionalLinkageTopo.add_node
    switchAndRouterMap["router"] = add_node(commonConfig.imageMap['ovs'],
                                            node_name="router",
                                            resource_limit={"cpu": "50", "mem": "1000"},
                                            location={"x": 110 * workerNum, "y": 300})

    linkageNum = 0
    ipNum = 0
    serverNode = serverAndWorkerMap["server"]
    serverIP = commonConfig.getIP("192.168.0.0", ipNum)
    ipNum += 1
    routerNode = switchAndRouterMap["router"]
    linkageName = commonConfig.getLinkageName(linkageNum)
    linkageNum += 1
    additionalLinkageTopo.add_link(serverNode, routerNode, linkageName, serverIP, "")
    print(f"add linkage between server({serverIP}) and router")
    switchID = 0
    for i in range(workerNum):
        if not ufs.isFather(i) or ufs.count(i) < 2:
            continue
        for workerID in ufs.member[i]:
            workerName = commonConfig.getWorkerName(workerID)
            workerNode = serverAndWorkerMap[workerName]
            workerIP = commonConfig.getIP("192.168.0.0", ipNum)
            ipNum += 1
            switchName = commonConfig.getSwitchName(switchID)
            switchNode = switchAndRouterMap[switchName]
            linkageName = commonConfig.getLinkageName(linkageNum)
            linkageNum += 1
            additionalLinkageTopo.add_link(workerNode, switchNode, linkageName, workerIP, "")
            print(f"add linkage between "
                  f"{commonConfig.getWorkerName(workerID)}({workerIP}) and "
                  f"{commonConfig.getSwitchName(switchID)}")
        switchID += 1
    for i in range(switchNum):
        switchNode = switchAndRouterMap[commonConfig.getSwitchName(i)]
        linkageName = commonConfig.getLinkageName(linkageNum)
        linkageNum += 1
        additionalLinkageTopo.add_link(routerNode, switchNode, linkageName, "", "")
        print(f"add linkage between router and {commonConfig.getSwitchName(i)}")
    for i in range(workerNum):
        if not ufs.isFather(i) or ufs.count(i) != 1:
            continue
        workerNode = serverAndWorkerMap[commonConfig.getWorkerName(i)]
        workerIP = commonConfig.getIP("192.168.0.0", ipNum)
        ipNum += 1
        linkageName = commonConfig.getLinkageName(linkageNum)
        linkageNum += 1
        additionalLinkageTopo.add_link(workerNode, routerNode, linkageName, workerIP, "")
        print(f"add linkage between {commonConfig.getWorkerName(i)}({workerIP}) and router")

    commonConfig.projectManager.deploy(projectName, additionalLinkageTopo)
    print(f"Deploy {projectName} successfully.")
    generateConfigFile(configList)


if __name__ == '__main__':
    argc = len(sys.argv)
    workerNum = None
    if argc < 2 or argc > 3:
        print("Usage: python createAdditionalLinkageTopo.py WOKER_NUM [ADDTIONAL_LINKAGE_NUM]")
        exit(1)
    else:
        workerNum = int(sys.argv[1])
        if argc == 3:
            addtionalLinkageNum = int(sys.argv[2])
        else:
            addtionalLinkageNum = 0
    if workerNum > 500 or workerNum < 1:
        print("WOKER_NUM must be in range [1, 500].")
        exit(1)
    if addtionalLinkageNum < 0 or addtionalLinkageNum > workerNum * (workerNum - 1) / 2:
        print("ADDTIONAL_LINKAGE_NUM is invalid, please check it.")
        exit(1)
    projectName = f'LM_{str(workerNum)}_{str(addtionalLinkageNum)}'
    commonConfig.init(projectName)
    projectList = commonConfig.projectManager.get_projects()
    if projectName in projectList:
        print(f"There has been a project named {projectName}, so process aborted.")
        exit(1)
    createAdditionalLinkageTopo()
    ret = prepareExperiment(projectName)
    if ret != 0:
        exit(ret)
    exit(updateBandwidth(projectName))
