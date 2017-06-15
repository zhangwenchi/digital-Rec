import numpy as np
import os

# traditional SVM can only judge the 1 or -1 question, so need some other knowledge

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
    testMat, testLabel = getInfo('TestFolder')



