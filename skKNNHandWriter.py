import numpy as np
from sklearn import neighbors
import os

def img2vec(filename):
    returnVec = np.zeros(1024)

    f = open(filename)
    for i in range(32):
        line = f.readline()
        for j in range(32):
            returnVec[i*32 + j] = int(line[j])

    return returnVec

if __name__ == '__main__':
    trainLabels = []
    trainFileList = os.listdir('trainingDigits')
    m = len(trainFileList)
    trainMat = np.zeros((m, 1024))

    for i in range(m):
        filename = trainFileList[i]
        trainLabels.append(int(filename.split('_')[0]))
        trainMat[i,:] = img2vec('trainingDigits/%s'%filename)

    testFileList = os.listdir('testDigits')
    errorCount = 0.0
    m = len(testFileList)
    testMat = np.zeros((m, 1024))
    testLabel = []

    for i in range(m):
        filename = testFileList[i]
        testLabel.append(int(filename.split('_')[0]))
        testMat[i,:] = img2vec('testDigits/%s'%filename)

    knn = neighbors.KNeighborsClassifier(n_neighbors=3)
    knn.fit(trainMat, trainLabels)
    print 'Finish fitting!'
    predict = knn.predict(testMat)
    print predict
    error = []
    for i in range(len(predict)):
        if predict[i] != testLabel[i]:
            error.append('Error is the:' + str(i))
            errorCount += 1.0

    print 'The error rate is ' + str(errorCount/m)
    error.append('The error rate is ' + str(errorCount/m))
    f = open('knn2Error','w')
    f.write(str(np.array(error)))
    f.close()

    f = open('testedLabel2.txt','w')
    f.write(str(predict))
    f.close()