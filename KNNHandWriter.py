import numpy as np
import os

global count

def getlens(x, y):
    sum = 0
    for i in range(len(x)):
        for j in range(len(x[0])):
            sum += (int(x[i][j])-int(y[i][j])) * (int(x[i][j])-int(y[i][j]))
    return sum

def getVector(path):

    Vector = []
    Label = []
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:
            f = open(path + '\\' + filename,'r')
            t = []
            lines = f.readlines()
            for line in lines:
                t.append(list(line[:-1]))
            f.close()
            Vector.append(t)

            Label.append(filename[0])

    return Vector, Label

def getTop(xArr, k): ### get top k max______sort or heap
    global count
    xArr.sort()
    print count
    count += 1
    #print xArr

    temp = np.zeros(10)
    for i in range(k):
        temp[xArr[i][1]] += 1
    index = -1
    max = 0
    for i in range(10):
        if max < temp[i]:
            max = temp[i]
            index = i
    return index

def knn(testVector, trainVector, trainLabel, k):
    global count
    count = 0
    bestLabel = []
    for i in range(len(testVector)):
        tbest = []
        for j in range(len(trainVector)):
            lens = getlens(testVector[i], trainVector[j])
            tbest.append([lens,trainLabel[j]])
        prediction = getTop(tbest, k)
        bestLabel.append(prediction)
    return bestLabel

def checkTraining(xlabel, ylabel):
    jishu = 0.0
    fenzi = 0.0
    for i in range(len(xlabel)):
        if xlabel[i] == int(ylabel[i]):
            jishu += 1
        else:
            print "Error is the %d"%i
            jishu += 1
            fenzi += 1
    return fenzi / jishu

if __name__ == '__main__':

    testpath = 'testDigits'
    #testpath = 'TestFolder'
    trainpath = 'trainingDigits'

    trainVector, trainLabel = getVector(trainpath)
    testVector, testLabel = getVector(testpath)

    trainingLabel = knn(testVector, trainVector, trainLabel, 3)
    ##print trainingLabel
    ##print testLabel
    f = open("testedLabel1.txt","w")
    f.write(str(np.array(trainingLabel)))
    f.close()

    errorRating = checkTraining(trainingLabel, testLabel)
    print errorRating
    print "The error rate is:" + str(errorRating)
