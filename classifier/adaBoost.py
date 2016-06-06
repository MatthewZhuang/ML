#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
AdaBoost algorithm
use decision tree to be the weak classifier
二分类组合算法,  只接受1 和 -1类
adaboost算法最后需要生成一组弱分类器, 和一组权重系数
"""
import numpy
from numpy import shape
from numpy import ones
from numpy import matrix
from numpy import mat
import math

def loadSimDat():
    dataMat = matrix([[1, 2.1, 1],
                      [2.0, 1.1, 1],
                      [1.3, 1.0, 0],
                      [1.0, 1.0, 1],
                      [2.0, 1.0, 1]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return dataMat, classLabels


def stumpClassify(dataMatrix, dimen, threshVal, ineq):
    '''
    弱分类器
    根据某个维度(节点dimen) 阈值(大于或者小于  ineq) 去做分类
    :param dataMatrix:
    :param dimen:
    :param threshVal:
    :param ineq:
    :return: 返回分类结果
    '''
    classArray = ones((shape(dataMatrix)[0], 1))
    if ineq == 'lt':
        classArray[dataMatrix[:, dimen] <= threshVal] = -1
    else:
        classArray[dataMatrix[:, dimen] > threshVal] = -1

    return classArray


def buildStump(dataArry, labels, D):
    '''
    构建决策树桩, 选取分类错误率最低的维度作为节点, 包括节点阈值的选取
    :param dataArry:  数据集
    :param labels:    对应类别
    :param D:         权重(开始为均值)
    :return:          决策树桩, 最小错误率, 分类结果
    '''
    dataMatrix = mat(dataArry)
    labelMat = mat(labels).T
    m, n = shape(dataMatrix)
    #对于连续值的步长
    numSteps = 10.0
    bestStump = {}
    bestClassEst = mat(numpy.zeros((m, 1)))
    minError = numpy.inf
    for i in range(n):
        rangemin = dataMatrix[:, i].min()
        rangemax = dataMatrix[:, i].max()
        stepSize = (rangemax - rangemin)/numSteps
        for j in range(-1, int(numSteps)+1):
            for inequal in ['lt', 'gt']:
                threshVal = (rangemin + float(j) * stepSize)
                predictVals = stumpClassify(dataMatrix, i, threshVal, inequal)
                errArr = mat(ones((m, 1)))
                errArr[predictVals == labelMat] = 0
                weightedErr = D.T * errArr
                if weightedErr < minError:
                    minError = weightedErr
                    bestClassEst = predictVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump, minError, bestClassEst


def adaBoostTrain(dataArr, labels, numIt = 40):
    '''

    :param dataArr: 数据集合
    :param labels:  类别标签
    :param numIt:   产生弱分类器的上限
    :return:       
    '''
    weakClasArr = []
    m, n = shape(dataArr)
    D = mat(ones((m, 1))/m)
    aggClassEst= mat(numpy.zeros((m, 1)))
    for i in range(numIt):
        bestStump, error, classEst = buildStump(dataArr, labels, D)
        #计算系数
        alpha = float(0.5 * math.log((1.0 - error)/max(error, 1e-16)))
        bestStump['alpha'] = alpha
        weakClasArr.append(bestStump)
        #重新给样本权重赋值, 详见公式
        expon = numpy.multiply(-1 * alpha * mat(labels).T, classEst)
        D = numpy.multiply(D, numpy.exp(expon))
        D = D / D.sum()
        aggClassEst += alpha * classEst
        aggErrors = numpy.multiply(numpy.sign(aggClassEst) != mat(labels).T, ones((m, 1)))
        errorRate= aggErrors.sum()/m
        print 'total error:', errorRate, '\n'
        if errorRate == 0.0:
            break
    return weakClasArr, aggClassEst


def adaClassify(dataToClass, classifiers):
    dataMatrix = mat(dataToClass)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(numpy.zeros((m, 1)))
    for i in range(len(classifiers)):
        classEst = stumpClassify(dataMatrix, classifiers[i]['dim'], classifiers[i]['thresh'], classifiers[i]['ineq'])
        aggClassEst += classifiers[i]['alpha'] * classEst
        print aggClassEst
    return numpy.sign(aggClassEst)


if __name__ == '__main__':
    # dataMatrix = matrix([[1, 2], [1, 1], [2, 4]])
    # dataMatrix = mat(dataMatrix)
    # print shape(dataMatrix)
    # classArray = ones((shape(dataMatrix)[0], 1))
    # print classArray

    #train set
    dataMat, classLabels = loadSimDat()
    weaks, est = adaBoostTrain(dataMat, classLabels, 9)
    print est
    #test
    print adaClassify([[1, 1, 1], [1, 1, 0]], weaks)





