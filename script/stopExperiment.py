#!/usr/bin/env python3

# Usage: python stopExperiment.py PROJECT_NAME

import sys
from commonConfig import *
import commonConfig
import os

def stopExperiment() -> None:
    nodeMap = commonConfig.nodeManager.get_nodes()
    while True:
        print(f'Kill or not?[y/N]:', end='')
        kill = input()
        if kill is None or len(kill) == 0:
            kill = 'n'
        if kill == 'y' or kill == 'n':
            break
    if kill == 'y':
        kill = True
    else:
        kill = False

    for nodeName in nodeMap:
        if "worker" not in nodeName and "server" not in nodeName:
            continue
        res = execCmd(nodeName, "bash -c \"ps -ef\"")
        output = None
        for cmd in res[nodeName]:
            output = res[nodeName][cmd]['output'].split('\n')
        if output is None:
            continue
        output = output[1:-1]
        pid = []
        for i in range(len(output)):
            if "python3" in output[i]:
                pid.append(output[i].split()[1])
        if len(pid) == 0:
            continue
        pidStr = " ".join(pid)
        print(pidStr)
        if kill:
            execCmd(nodeName, f"kill -9 {pidStr}")
    #  stop updateBandwidth.py script
    if kill:
        os.system(f"pgrep -f '{projectName}' | xargs kill -9")

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 2:
        print("Usage: python stopExperiment.py PROJECT_NAME")
        exit(-1)
    else:
        projectName = sys.argv[1]
    init(projectName)
    if projectName not in commonConfig.projectManager.get_projects():
        print(f"project {projectName} doesn't exists, please check it.")
        exit(-1)
    stopExperiment()
