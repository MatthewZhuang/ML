if __name__ == '__main__':
    # pcti = [1] * 2
    # pct = [pcti for i in range(3)]
    # print pct[2][1]
    # print 1/float(2)
    #
    # pc = [0]*5
    # pc[0:3] = [1]*3
    # pc[3:5] = [2]*2
    # print pc
    # import re
    # s = 'hello999.'
    # res = re.findall('[0-9\.]', s)
    # for re in res:
    #     s = s.replace(re, '')
    # print s
    #
    #
    # for i in range(10):
    #     print i
    pcti = [0]*9
    pct_tmp = [pcti for i in range(9)]
    print  pct_tmp
    d = {}
    d['h'] = 'hello'
    l = []
    l.append(d)
    print l[0]['h']

    files = open("/Users/Matthew/Documents/python/data/zkread/internetfinance.txt", 'r')
    c1 = files.readlines()
    print len(c1)
    # files = open("/Users/Matthew/Documents/python/data/Project Annual Review/1.txt", 'r')
    # c2 = files.readlines()
    # print len(c2)
    from DataPreProcess import cut_words
    segwords1 = cut_words(c1)
    file1 = "/Users/Matthew/Documents/python/data/zkread/segwords.txt"
    # segwords1 = loadSegFile(file1)
    from DataPreProcess import writeSegResult
    writeSegResult(segwords1, file1)