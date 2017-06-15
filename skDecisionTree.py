import numpy as np
import os
import pydotplus

## sklearn use the pixel to get the decision tree
from sklearn import tree

def getInfo(dir):

    fileList = os.listdir(dir)
    m = len(fileList)

    returnMat = np.zeros((m,1024))
    returnLabel = []

    for i in range(m):
        returnLabel.append(int(fileList[i].split('_')[0]))
        temp = np.zeros(1024)
        f = open('%s/%s'%(dir,fileList[i]))
        for j in range(32):
            x = f.readline()
            for k in range(32):
                temp[j*32+k] = int(x[k])
        returnMat[i,:] = temp
    return returnMat, returnLabel


if __name__ == '__main__':

    trainMat, trainLabel = getInfo('trainingDigits')
    testMat, testLabel = getInfo('testDigits')

    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf.fit(trainMat, trainLabel)

    x = clf.predict(testMat)

    error = 0.0

    f = open('dt2Error','w')

    for i in range(len(testLabel)):
        if testLabel[i] != x[i]:
            f.write("error is :" + str(i) + '\n')
            error += 1.0
    print "error rate is :" + str(error/len(testLabel))
    f.write("error rate is :" + str(error/len(testLabel)))
    f.close()


    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf("DecisionTree.pdf")



