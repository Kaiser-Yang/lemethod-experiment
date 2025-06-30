#!/usr/bin/env python3

# Usage: python prepareExperiment.py PROJECT_NAME

import commonConfig
from commonConfig import uploadFileToNode
from commonConfig import getWorkerName
import sys


def uploadExperimentFileToAllNode(workerNum: int) -> None:
    uploadFileToNode("./experiment.py", "server", "/root/experiment.py")
    uploadFileToNode("./start_server.sh", "server", "/root/start_server.sh")
    uploadFileToNode("./start_scheduler.sh", "server", "/root/start_scheduler.sh")
    for i in range(workerNum):
        uploadFileToNode("./experiment.py", getWorkerName(i), "/root/experiment.py")
        uploadFileToNode("./start_worker.sh", getWorkerName(i), "/root/start_worker.sh")


def prepareExperiment(projectName: str) -> int:
    commonConfig.init(projectName)
    if projectName not in commonConfig.projectManager.get_projects():
        print(f"project {projectName} doesn't exists, please check it.")
        return 1
    workerNum = 0
    for nodeName in commonConfig.nodeManager.get_nodes():
        if "worker" in nodeName:
            workerNum += 1
    uploadExperimentFileToAllNode(workerNum)
    return 0


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 2:
        print("Usage: python prepareExperiment.py PROJECT_NAME")
        exit(1)
    else:
        projectName = sys.argv[1]
    exit(prepareExperiment(projectName))
