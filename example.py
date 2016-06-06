import numpy

def loadDataSet():
    postingList=[
        ['my', 'my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWord2Vec(vocabList,inputData):
    returnVec = [0] * len(vocabList)
    for document in inputData:
        if document in vocabList:
            returnVec[vocabList.index(document)] = 1
        else:
            print "the word: %s is not in my Vocabyulary!" %document
    return returnVec


def trainNB(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p1Vector = numpy.ones(numWords)
    p0Vector = numpy.ones(numWords)
    p1DocumentWords = 2
    p0DocumentWords = 2

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Vector += trainMatrix[i]
            p1DocumentWords += sum(trainMatrix[i])
        else:
            p0Vector += trainMatrix[i]
            p0DocumentWords += sum(trainMatrix[i])

    p1 = p1Vector/p1DocumentWords
    p0 = p0Vector/p0DocumentWords

    return pAbusive, numpy.log(p1), numpy.log(p0)



if __name__ == '__main__':
    articles, cs = loadDataSet()
    words = createVocabList(articles)
    p1 = numpy.ones(10)
    print type(p1)

    p1 = numpy.ones(10)
    p1 = p1 + 9
    p1 = numpy.log(p1)
    print p1

