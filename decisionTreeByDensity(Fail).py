##the picture is 32*32, I make all the area 8*8

from math import log
import os
import numpy as np

def shannonEnt(dic):
    mm = {}
    dicLen = len(dic)
    ent = 0.0
    for ele in dic:
        mm[ele] = mm.get(ele,0) + 1   ### if not have, just create it
    for key in mm:
        prob = float(mm[key]) / dicLen
        ent -= prob * log(prob, 2)
    return ent

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

def splitMat(mat, n):
    x = 32 / n
    matLen = len(mat)
    returnMat = np.zeros((x*x, 1024 * matLen / x / x))
    index = np.zeros(x*x)
    for line in range(matLen):
        for k in range(1024):
            kx = k % 32
            ky = k / 32
            tindex = kx/n + (ky/n * x)
            returnMat[tindex, index[tindex]] = mat[line, k]
            index[tindex] += 1
    return returnMat

def getEnt(mat):
    entVec = []
    for i in range(len(mat)):
        entVec.append(shannonEnt(mat[i]))

    x = np.array(entVec)
    #print x
    return np.argsort(x)

def splitVec(vec, n):
    x = 32 / n
    returnMat = np.zeros((x*x, 1024 / x / x))
    index = np.zeros(x*x)
    for k in range(1024):
        kx = k % 32
        ky = k / 32
        tindex = kx/n + (ky/n * x)
        returnMat[tindex, index[tindex]] = vec[k]
        index[tindex] += 1
    return returnMat


def getFeature(mat):
    returnMat = []
    for i in range(len(mat)):
        w = splitVec(mat[i], 8)
        tempV = []
        for i in range(32/8 * 32/8):
            sum = 0
            for j in range(len(w[i])):
                if w[i,j] == 1:
                    sum += 1
            tempV.append(sum)
        returnMat.append(np.array(tempV))
    return np.array(returnMat)

def updateByEnt(trainFeature, EntValue):
    for i in range(len(trainFeature)):
        x = np.zeros(len(EntValue))
        for j in range(len(EntValue)):
            x[j] = trainFeature[i][EntValue[j]]
        x = np.array(x)
        for j in range(len(EntValue)):
            trainFeature[i][j] = x[j]
    return trainFeature

def getRange(feature, labels):
    shuMat = [[] for i in range(10)]
    for num in range(10):
        for i in range(len(labels)):
            if labels[i] == num:
                shuMat[num].append(feature[i])

    featureRange = [[] for i in range(10)]

    for num in range(10):
        tRange = [[] for i in range(16)]
        for i in range(len(shuMat[num])):
            for fea in range(16):               ####suppose 8*8
                tRange[fea].append(shuMat[num][i][fea])
        for j in range(16):
            tRange[j].sort()
            x = list(set(tRange[j]))
            #print x
            if len(x) > 6:
                del x[:3]
                del x[-3:]
            max = x[-1]
            min = x[0]
            featureRange[num].append((min,max))
    return featureRange



def createTree(feature, labels):
    tree = {}
    return tree

if __name__ == '__main__':

    trainMat, trainLabel = getInfo('trainingDigits')
    testMat, testLabel = getInfo('testDigits')
    testMat, testLabel = getInfo('TestFolder')

    ##separate the dataset to 16 regions( every is 8 * 8 )
    trainSplitMat = splitMat(trainMat, 8)
    #np.savetxt("teeeeest", testSMat,  fmt="%d")
    EntValue = getEnt(trainSplitMat)
    print "Best feature is :" + str(EntValue)
    #### the feature is based on the density
    trainFeature = getFeature(trainMat)
    #print trainFeature
    trainFeature = updateByEnt(trainFeature, EntValue)
    #print trainFeature          ###already get all the feature!!!!, one to one the label !!!!!
    trainF = getRange(trainFeature, trainLabel)
    ### get the Range of the density of every number

    print trainF
'''
We can see that the density is so lame that we totally can not judge the numbers by it.
Maybe sklearn can give me a better answer......
Desicion Tree I should learn it later, as well as C4.5

'''

