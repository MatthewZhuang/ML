#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
this class is for feature extraction

KL distance. or relative entropy

coordination with chi-square

像KL  chi-square  textRank这样的算法可以找出具体的特征词
但是想LSA和plsa, PCA这样的降为方法只是起到降维作用,并不能找出具体的特征词

"""
import jieba
import math
import re
def cut_words(articles):
    '''
    seg words, you should save the result to the disk.
    :param articles:
    :return:
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
    :return:
    '''
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def featureExtractKL(articles, cateVec, allwords):
    '''
    method: KL with chi-square
    pt : 特征t出现的概率
    pc : 类别C出现的概率
    pct : 在特征t出现的前提下,属于C的概率
    num_c : the number of classes
    cd: 类别c中出现t的数目/全部文本中出现t的数目
    dd: 类别c中出现t的数目/类别C的总数目
    relative entroy with chi-square
    :param clas: multi classes
    :return:
    '''
    num_c = cateVec[len(cateVec)-1]+1
    #存储每个单词出现的文章数
    pt_tmp = [0]*len(allwords)
    pt = [0] * len(allwords)
    i = 0
    sum_article = len(articles)

    for word in allwords:
        fre = 0
        for article in articles:
            if article.count(word) > 0:
                fre += 1
        pt_tmp[i] = fre
        i += 1
    pt = [pt_tmp[i]/float(sum_article) for i in range(len(pt_tmp))]

    pc = [0]*num_c
    pc_tmp = [0]*num_c
    for i in range(num_c):
        pc_tmp[i] = cateVec.count(i)
    pc = [pc_tmp[i]/float(num_c) for i in range(len(pc_tmp))]

    pcti = [0]*num_c
    # cdti = [0]*num_c
    # ddti = [0]*num_c
    #记录每个关键词在每个类别下面出现的文章数
    pct_tmp = [pcti for i in range(len(allwords))]
    pct = [pcti for i in range(len(allwords))]
    # cdt = [cdti for i in range(len(allwords))]
    # ddt = [ddti for i in range(len(allwords))]
    for j in range(len(allwords)):
        count = 0
        for i in range(len(articles)):
            if articles[i].count(word) > 0:
                c = cateVec[i]
                pct_tmp[j][c] += 1
                count += 1
        pct[j] = [pct_tmp[j][z]/(float(count)+1) for z in range(num_c)]

    num_words = len(allwords)
    ece = [0]*num_words
    for i in range(num_words):
        sum_c = 0
        for c in range(num_c):
            cd = pct_tmp[i][c]/pt_tmp[i]
            dd = pct_tmp[i][c]/pc_tmp[c]
            sum_c += pct[i][c]*math.log((pct[i][c]+1)/(pc[c]+2))*cd*dd
        ece[i] = pt[i]*sum_c

    keywords = []
    for i in range(len(ece)):
        if ece[i] > 866000000:
            keywords.append(allwords[i])
            print allwords[i] + " " + str(ece[i])

    return keywords


def adaBoost():
    '''
    boosting algorithm
    若分类器的选择:
    决策树\NB\SVM\LR\

    暂时采用LR?
    :return:
    '''
    pass



def train(articles, cateVector):
    '''
    model training .
    :param articles:
    :param cateVector:
    :return:
    '''
    allwords = createVocabList(articles)
    keywords = featureExtractKL(articles, cateVector, allwords)

    #use keywords to decrease the dimension





if __name__ == '__main__':
    files = open("/Users/Matthew/Documents/python/data/SQA/1.txt", 'r')
    c1 = files.readlines()
    files = open("/Users/Matthew/Documents/python/data/Project Annual Review/1.txt", 'r')
    c2 = files.readlines()
    print len(c2)

    segwords1 = cut_words(c1)
    class1 = len(segwords1)
    segwords2 = cut_words(c2)
    class2 = len(segwords2)
    articles = []
    articles.extend(segwords1)
    articles.extend(segwords2)

    cateVec = [1]*(class1+class2)
    #切片赋值
    cateVec[0:class1] = [0]*class1

    train(articles, cateVec)
