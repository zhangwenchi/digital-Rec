## so time cosuming!!!!!!!!

import numpy as np
import os
from math import log
import operator

count = 0



def getInfo(dir):

    fileList = os.listdir(dir)
    m = len(fileList)

    returnMat = np.zeros((m, 1024))
    returnLabel = []

    for i in range(m):
        returnLabel.append(int(fileList[i].split('_')[0]))
        temp = np.zeros(1024)
        f = open('%s/%s'%(dir,fileList[i]))
        for j in range(32):
            x = f.readline()
            for k in range(32):
                temp[j*32 + k] = int(x[k])
        returnMat[i,:] = temp
    return returnMat, returnLabel

def getShannonEnt(data, label):
    numEntries = len(data)
    labelCounts = {}
    for count in range(len(label)):
        if label[count] not in labelCounts.keys():
            labelCounts[label[count]] = 0
        labelCounts[label[count]] += 1

    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitData(data, axis, value):
    returnMat = []
    for vec in data:
        if vec[axis] == value:
            x = vec[:axis]
            x = np.append(x, vec[axis+1:])
            returnMat.append(x)
    return returnMat

def chooseBestFeature(data, lable):
    numOfFeature = len(data[0])
    bestFeature = -1
    bestInfoGain = 100.0

    for i in range(numOfFeature):
        featList = [example[i] for example in data]
        uniqueValues = set(featList)
        newGain = 0.0
        for unival in uniqueValues:
            x = splitData(data, i, unival)
            prob = float(len(x)) / len(data)
            newGain -= prob * getShannonEnt(x, lable)

        if newGain < bestInfoGain:
            bestInfoGain = newGain
            bestFeature = i

    return bestFeature

def getMajCount(classList):

    classDict = {}
    for cla in classList:
        if cla not in classDict.keys():
            classDict[cla] = 0
        classDict[cla] += 1
    sortedClassCnt = sorted(classDict.iteritems(), key=operator.itemgetter(1), reverse=True )
    return sortedClassCnt[0][0]

def createTree(data, labels):

    global count
    numOfLabels = set(labels)
    if numOfLabels == 1:               ##all is the same label
        return labels[0]
    if len(data[0]) == 1:             ## do not have more features
        return getMajCount(labels)

    bestFeature = chooseBestFeature(data, labels)
    print 'The best feature is :' + str(bestFeature)

    myTree = {bestFeature:{}}
    featVal = [example[bestFeature] for example in data]
    uniqueVal = set(featVal)
    for val in uniqueVal:
        subLabels = labels[:]
        print "The tree:" + str(count)
        count += 1
        myTree[bestFeature][val] = createTree(splitData(data, bestFeature, val), subLabels)


    return myTree





if __name__ == '__main__':

    trainMat, trainLabel = getInfo('trainingDigits')
    testMat, testLabel = getInfo('testDigits')
    testMat, testLaebl = getInfo('TestFolder')

    myTree = createTree(trainMat, trainLabel)
    print myTree
