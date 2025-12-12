#!/usr/bin/env python3

#Usage: python extractResult.py PROJECT_NAME [OUTPUT_PREFIX]

import sys
from commonConfig import *
import commonConfig
import os

def extractResult():
    nodeMap = commonConfig.nodeManager.get_nodes()
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    for nodeName in nodeMap:
        if "worker" in nodeName:
            res = execCmd(nodeName, "cat /root/experimentResult.out")
            print(res[nodeName][f"0_cat /root/experimentResult.out"]["output"])
            with open(savePath + "/" + nodeName, "w") as resFile:
                resFile.write(res[nodeName][f"0_cat /root/experimentResult.out"]["output"])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2 or argc > 3:
        print("Usage: python extractResult.py PROJECT_NAME [OUTPUT_PREFIX]")
        exit(1)
    projectName = sys.argv[1]
    if argc >= 3:
        savePath = sys.argv[2]
    else:
        savePath = "./"
    init(projectName)
    if projectName not in commonConfig.projectManager.get_projects():
        print(f"project {projectName} does not exist, please check it.")
        exit(1)
    extractResult()
