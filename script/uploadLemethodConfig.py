#!/usr/bin/env python

import commonConfig
import sys

def uploadLemethodConfig(projectName, filePath):
    commonConfig.init(projectName)
    if projectName not in commonConfig.projectManager.get_projects():
        print(f"project {projectName} doesn't exists, please check it.")
        return 1
    for nodeName in commonConfig.nodeManager.get_nodes():
        commonConfig.uploadFileToNode(filePath, nodeName, "/root/lemethod.conf")
    return 0


if __name__ == "__main__":
    argc = len(sys.argv);
    if argc != 3:
        print("Usage: python uploadCalculationTime.py PROJECT_NAME DIR")
        exit(1)
    projectName = sys.argv[1];
    filePath = sys.argv[2];
    exit(uploadLemethodConfig(projectName, filePath))

