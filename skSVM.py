import numpy as np
import os
from sklearn import svm


def getInfo(dir):

    fileList = os.listdir(dir)
    m = len(fileList)

    returnMat = np.zeros((m, 1024))
    returnLabel = []

    for k in range(m):
        returnLabel.append(int(fileList[k].split('_')[0]))
        f = open('%s/%s'%(dir, fileList[k]))
        temp = np.zeros(1024)
        for i in range(32):
            x = f.readline()
            for j in range(32):
                temp[i*32+j] = x[j]
        returnMat[k,:] = temp

    return returnMat, returnLabel


if __name__ == '__main__':

    trainMat, trainLabel = getInfo('trainingDigits')
    testMat, testLabel = getInfo('testDigits')

    clk = svm.SVC()
    clk.fit(trainMat,trainLabel)
    predict = clk.predict(testMat)

    error = []
    errorCount = 0.0

    for i in range(len(predict)):
        if predict[i] != testLabel[i]:
            error.append('Error is the:' + str(i))
            errorCount += 1.0

    print 'The error rate is ' + str(errorCount/len(testLabel))
    error.append('The error rate is ' + str(errorCount/len(testLabel)))
    f = open('SVMError','w')
    f.write(str(np.array(error)))
    f.close()

    f = open('testedLabel3.txt','w')
    f.write(str(predict))
    f.close()