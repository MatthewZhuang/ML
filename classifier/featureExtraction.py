# -*- coding:UTF-8 -*-
import math

def KL(articles, cateVec, allwords, topK):
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
        word = allwords[j]
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
    # for i in range(len(ece)):
    #     if ece[i] > 866000000:
    #         keywords.append(allwords[i])
    #         print allwords[i] + " " + str(ece[i])

    words = {}
    for i in range(len(ece)):
        words[allwords[i]] = ece[i]

    sorted(words.items(), lambda x, y: cmp(x[1], y[1])),

    i = 0
    for key, value in words.items():
        keywords.append(key)
        i = i + 1
        if i > topK:
            break

    return keywords


def IG(articles, cateVec, allwords, topK):
    '''
    特征词选择算法, 信息增益法
    :param articles:
    :param cateVec:  0, 0, 0, 1, 1, 2, 3, 4
    :param allwords:
    :param topK:
    :return:
    '''
    ig = {}

    entropy = 0
    num_c = cateVec[len(cateVec) - 1] + 1
    pc = [0]*num_c
    for i in range(num_c):
        pc[i] = cateVec.count(i)/float(num_c)

    for i in range(num_c):
        entropy += -1 * pc[i] * math.log(max(pc[i], 1e-16))

    pt_tmp = [0] * len(allwords)
    for j in range(len(allwords)):
        fre = 0
        word = allwords[j]
        for article in articles:
            if article.count(word) > 0:
                fre += 1
        pt_tmp[j] = fre
        i += 1
    pt = [pt_tmp[i] / float(len(articles)) for i in range(len(pt_tmp))]

    pcti = [0] * num_c
    pct_tmp = [pcti for i in range(len(allwords))]
    pct = [pcti for i in range(len(allwords))]
    for j in range(len(allwords)):
        count = 0
        word = allwords[j]
        for i in range(len(articles)):
            if articles[i].count(word) > 0:
                c = cateVec[i]
                pct_tmp[j][c] += 1
                count += 1
        pct[j] = [pct_tmp[j][z] / (float(count) + 1) for z in range(num_c)]


    for j in range(len(allwords)):
        sum1 = 0
        sum2 = 0
        for c in range(num_c):
            sum1 += math.log(max(pct[j][c], 1e-16)) * pc[c]
            sum2 += math.log(max((1 - pct[j][c]), 1e-16)) * (1 - pc[c])
        igt = -entropy + pt[j]*sum1 + (1-pt[j])*sum2
        ig[allwords[j]] = igt

    sorted(ig.items(), lambda x, y: cmp(x[1], y[1])),

    i = 0
    keywords = []
    for key, value in ig.items():
        keywords.append(key)
        i = i + 1
        if i > topK:
            break

    return keywords





