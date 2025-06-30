#!/usr/bin/env python3

# Usage: python uploadCalculationTime.py PROJECT_NAME DIR
import sys
import commonConfig
import os

def uploadCalculationTime(projectName, directory):
    commonConfig.init(projectName)
    if projectName not in commonConfig.projectManager.get_projects():
        print(f"project {projectName} doesn't exists, please check it.")
        return 1
    workerNum = 0
    for nodeName in commonConfig.nodeManager.get_nodes():
        if "worker" in nodeName:
            workerNum += 1
    fileNum = 0
    for item in os.listdir(directory):
        itemPath = os.path.join(directory, item)
        if os.path.isfile(itemPath) and item.startswith("worker"):
            commonConfig.uploadFileToNode(itemPath, item[0:7], "/root/calculationTimeFile.txt")
            fileNum += 1
    if fileNum != workerNum:
        print(f"File number is not equal to worker number, please check it.")
        return 1
    return 0


if __name__ == "__main__":
    argc = len(sys.argv);
    if argc != 3:
        print("Usage: python uploadCalculationTime.py PROJECT_NAME DIR")
        exit(1)
    projectName = sys.argv[1];
    directory = sys.argv[2];
    exit(uploadCalculationTime(projectName, directory))
