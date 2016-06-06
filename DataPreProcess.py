#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
this module is for the data preprocess.
"""
import re
import jieba
import math
from numpy import matrix
def loadFile(filename):
    '''
    every line is one article.
    :param filename:
    :return: list()
    '''
    files = open(filename, 'r')
    articles = files.readlines()
    files.close()
    return articles

def cut_words(articles):
    '''
    seg words, you should save the result to the disk.
    :param articles:
    :return: list(list())
    '''
    res = []
    for article in articles:
        #article = article.replace('\t', ' ').replace('\t', ' ').replace(',', ' ')
        re_list = re.findall('[0-9\.]', article)
        for result in re_list:
            article = article.replace(result, " ")
        res_article = []
        seg_article = jieba.cut(article)
        for a in seg_article:
            if len(a) > 1 and a is not '\t':
                res_article.append(a)
        res.append(res_article)
    return res

def createVocabList(dataSet):
    '''
    get all the words in the corpus
    :param dataSet:
    :return: list()
    '''
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def createVSM(articles, keywords):
    '''
    use keywords or allwords to createVSM
    if use allwords, you can use PCA, SVD to decrease
    use numpy narray
    word exist 1  not 0     离散的
    tfidf    值是连续的
    :param articles:
    :param keywords:
    :return:
    '''
    mat = []
    for article in articles:
        a = []
        for word in keywords:
            if article.count(word) > 0:
                a.append(1)
            else:
                a.append(0)
        mat.append(a)
    return matrix(mat), mat, a



def featureExtract(articles, cateVec, allwords, topK):
    '''
    keywords extraction
    :param articles:  list(list())
    :param cateVec:   list()
    :param allwords:  list()
    :param topK:      int
    :return:
    '''
    from featureExtraction import KL
    from featureExtraction import IG
    keywords = IG(articles, cateVec, allwords, topK)
    return keywords


def writeVSMFile(articlename, articles, wordname, words, c):
    '''
    write the segment result into the file.
    article_format: weight1,weight2....weightn|class(0,1,...)
    word_format: word1,word2,word3......
    :param filename:
    :return: void
    '''
    files = open(articlename, 'a')
    for article in articles:
        res = ','.join(article) + "|" + str(c)
        files.write(res)
        files.write("\n")
    files = open(wordname, 'w')
    res = ','.join(words)
    files.write(res)
    files.close()

def writeSegResult(articles, filename):
    files = open(filename, 'w')
    for article in articles:
        res = ','.join(article)
        files.write(res.encode('utf-8'))
        files.write("\n")
    files.close()

def loadSegFile(filename):
    file = open(filename, 'r')
    files = file.readlines()
    articles = []
    for line in files:
        articles.append(line.split(','))
    file.close()
    return articles


if __name__ == '__main__':
    # files = open("/Users/Matthew/Documents/python/data/SQA/1.txt", 'r')
    # c1 = files.readlines()
    # print len(c1)
    # files = open("/Users/Matthew/Documents/python/data/Project Annual Review/1.txt", 'r')
    # c2 = files.readlines()
    # print len(c2)

    # segwords1 = cut_words(c1)
    file1 = "/Users/Matthew/Documents/python/data/zkread/segwords.txt"
    segwords1 = loadSegFile(file1)
    # writeSegResult(segwords1, file1)

    class1 = len(segwords1)
    # segwords2 = cut_words(c2)
    file2 = "/Users/Matthew/Documents/python/data/SQA/segwords.txt"
    # writeSegResult(segwords2, file2)
    segwords2 = loadSegFile(file2)
    class2 = len(segwords2)
    articles = []
    articles.extend(segwords1)
    articles.extend(segwords2)

    cateVec = [1] * (class1 + class2)
    # 切片赋值
    cateVec[0:class1] = [0] * class1

    allwords = createVocabList(articles)
    keywords = featureExtract(articles, cateVec, allwords, 100)

    for word in keywords:
        print word

    cateVec = [-1] * (class1 + class2)
    # 切片赋值
    cateVec[0:class1] = [1] * class1
    vsm, mat, test = createVSM(articles, keywords)
    from adaBoost import adaClassify
    from adaBoost import adaBoostTrain
    weaks, est = adaBoostTrain(mat, cateVec, 9)

    print adaClassify(mat, weaks)

