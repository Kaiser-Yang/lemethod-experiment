#!/usr/bin/env python3

# Usage: python3 extractor.py

import os

if __name__ == '__main__':
    fileSet = set(os.listdir('./'))
    totalTimeMap = {}
    for fileOrDir in fileSet:
        if fileOrDir == '.' or fileOrDir == '..':
            continue
        if os.path.isfile('./' + fileOrDir):
            continue
        workerNum = 0
        dataFileSet = set(os.listdir('./' + fileOrDir))
        for dataFile in dataFileSet:
            if dataFile[0:6] == 'worker' and len(dataFile) == 7:
                workerNum += 1
        startTime = -1
        endTime = -1
        resultList = None
        for i in range(workerNum):
            fileName = './' + fileOrDir + '/worker' + str(i)
            data = open(fileName, 'r')
            lineList = data.readlines()
            epoch = len(lineList)
            if resultList == None:
                resultList = [[-1., -1.] for _ in range(epoch)]
            for j in range(epoch):
                line = lineList[j].split()
                if startTime == -1:
                    startTime = float(line[0])
                    endTime = float(line[1])
                startTime = min(startTime, float(line[0]))
                endTime = max(endTime, float(line[1]))
                resultList[j][0] = max(resultList[j][0], float(line[0]))
                resultList[j][1] = max(resultList[j][1], float(line[1]))
            data.close()
        resultFile = open('./' + fileOrDir + '/iteration', 'w')
        assert(resultList != None)
        for item in resultList:
            resultFile.write(f'{item[1] - item[0]}\n')
        resultFile.write(f'{endTime - startTime}\n')
        resultFile.close()
        totalTimeMap[fileOrDir] = endTime - startTime;
    for item in totalTimeMap.items():
        print(item)

