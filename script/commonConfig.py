#!/usr/bin/env python3

from typing import Optional
from vemu_api import CmdManager, ImageManager, LinkManager, NodeManager, ProjectManager
from vemu_api import Topo, Image

userName = 'kaiser'
backendURL = 'kb310server.x3322.net'
backendPort = 10435

imageManager = None
projectManager = None
nodeManager = None
linkManager = None
cmdManager = None
imageMap = None

netMaskLen = 19


def getWorkerName(id: int) -> str:
    return "worker" + str(id)


def getLinkageName(i: int) -> str:
    return "linkage" + str(i)


def getSwitchName(i: int) -> str:
    return "switch" + str(i)


def getIP(networkIP: str, index: int) -> str:
    index += 1
    ipNum = list(map(int, networkIP.split('.')))
    assert(len(ipNum) == 4)
    res = ""
    for i in range(4):
        i += 1
        if i == 1:
            ipNum[-i] += index
        if i + 1 <= 4:
            ipNum[-(i + 1)] += ipNum[-i] // 256
        ipNum[-i] %= 256
    for i in range(4):
        res += str(ipNum[i])
        if i != 3:
            res += "."
    res += "/" + str(netMaskLen)
    return res


def createServerAndWorker(topo: Topo, nodeType: Image, workerNum: int) -> dict:
    nodeMap = {}
    nodeMap["server"] = topo.add_node(nodeType, node_name="server",
                                      resource_limit={"cpu": "0", "mem": "0"},
                                      location={"x": 110 * workerNum, "y": 400})
    for i in range(workerNum):
        workerName = getWorkerName(i)
        nodeMap[workerName] = topo.add_node(nodeType, node_name=workerName,
                                            resource_limit={"cpu": "0", "mem": "0"},
                                            location={"x": 220 * i, "y": 100})
    return nodeMap


def createSwitchNode(topo: Topo, nodeType: Image, switchNum: int) -> dict:
    nodeMap = {}
    for i in range(switchNum):
        switchName = getSwitchName(i)
        nodeMap[switchName] = topo.add_node(nodeType, node_name=switchName,
                                            resource_limit={"cpu": "0", "mem": "0"},
                                            location={"x": 220 * i, "y": 200})
    return nodeMap


def init(projectName: Optional[str]) -> None:
    global imageManager, projectManager, imageMap
    imageManager = ImageManager(userName, backendURL, backendPort)
    projectManager = ProjectManager(userName, backendURL, backendPort)
    imageMap = imageManager.get_images()
    global nodeManager, linkManager, cmdManager
    nodeManager = NodeManager(userName, projectName, backendURL, backendPort)
    linkManager = LinkManager(userName, projectName, backendURL, backendPort)
    cmdManager = CmdManager(userName, projectName, backendURL, backendPort)


def checkCmdExecResult(result: dict, nodeName: str):
    for key in result[nodeName]:
        if result[nodeName][key]["exit_code"] != 0:
            print("errors occured while exec cmd:")
            print(result[nodeName][key])
            exit(-1)


def execCmd(node: str, cmd: str) -> dict:
    assert(cmdManager != None)
    print(f"exec cmd {cmd} on {node}.")
    result = cmdManager.exec_cmds_in_nodes({node: [cmd]}, "10", "true")
    checkCmdExecResult(result, node)
    return result


def uploadFileToNode(fileName: str, node: str, saveFileName: str):
    execCmd(node, f"rm -rf {saveFileName}")
    with open(fileName, 'r') as file:
        content = file.read()
        # HACK:
        # Weird escape characters, may need to be fixed in the future
        content = content.replace("\\", "\\\\\\\\")
        content = content.replace('"', '\\\\\\"')
        content = content.replace("$", "\\$")
        execCmd(node, f'bash -c "echo \\"{content}\\" >> {saveFileName}"')
