#!/usr/bin/env python
import optparse
import sys
from operator import itemgetter

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="infile", default="dex-tag.txt", help="input")
optparser.add_option("-o", "--output", dest="outfile", default="out.txt", help="output")
optparser.add_option("-t", "--thresh", dest="th_top", default=20, type="int", help="freq")
optparser.add_option("-s", "--scoreOut", dest="s_out", default="score.txt",  help="score")

(opts, _) = optparser.parse_args()

th_top = opts.th_top
outfile = opts.outfile
infile = opts.infile
scoreout = opts.s_out


def convert(dic):
    ls = []
    for each in dic:
        ls += [(each, dic[each])]
    return ls
def convertToDic(ls):
    dic = {}
    for each in ls:
        dic[each[0]] = each[1]
    return dic
def reassemble(lst):
    s = ''
    for i in eval(lst):
        s += i[0] 
        s += ' '
    return s.lower() 

    
tags = ['CC', #coordinating conjunction
        'CD', #cardinal number
        'FW', #foreign word
        'JJ', #Adj
        'JJR', #adj-er
        'JJS', #
        'MD',#can/could
        'NN',
        'NNS',
        'NNP',
        'NNPS',
        'RB',
        'RBR',
        'RBS',
        'VB',
        'VBD',
        'VBG',
        'VBN',
        'VBP',
        'VBZ',
        'WDT',
        'WP',
        'WP$',
        'WRB',
        'DT', 
        'EX',
        'IN',#that
        'LS',
        'PDT', #0.5
        'POS',
        'PRP',
        'PRP$',
        'RP',
        'SYM',
        'TO',
        'UH']

weightDic = {'CC' : 0.6, 'CD': 1, 'FW': 0.1, 'JJ': 1, 'JJR':1, 'JJS':1, 'MD': 0.6,
             'NN': 1, 'NNS':1, 'NNP':1, 'NNPS':1, 'RB':1, 'RBR':1,'RBS':1,
             'VB':1,'VBD':1,'VBG':1,'VBN':1,'VBP':1,'VBZ':1,
             'WDT':0.6, 'WP':0.8, 'WP$':0.8,'WRB':0.7,'DT':0.1, # was 0.1
             'EX': 1, 'IN':0.4,
             'LS':0.2,
             'PDT':0.5,
             'POS':0.05,
             'PRP':0.05,
             'PRP$':0.05,
             'RP':0.2,
             'SYM':1,
             'TO':0.5,
             'UH':0.1}
    # tags = ['CC', #coordinating conjunction
    #         'CD', #cardinal number
    #         'FW', #foreign word
    #         'JJ', #Adj
    #         'JJR', #adj-er
    #         'JJS', 'MD',#can/could
    #         'NN','NNS','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB','EX',
    #         'IN',#that
    #         'PDT'] #0.5 

    # weightDic = {'CC' : 0.6, 'CD': 1, 'FW': 1, 'JJ': 1, 'JJR':1, 'JJS':1, 'MD': 0.6,
    #          'NN': 1, 'NNS':1, 'NNP':1, 'NNPS':1, 'RB':1, 'RBR':1,'RBS':1,
    #          'VB':1,'VBD':1,'VBG':1,'VBN':1,'VBP':1,'VBZ':1,
    #          'WDT':0.6, 'WP':0.8, 'WP$':0.8,'WRB':0.7,'DT':0.1,
    #          'EX': 0.8, 'IN':0.4,
    #          'LS':0.2,
    #          'PDT':0.5,
    #          'POS':0.05,
    #          'PRP':0.05,
    #          'PRP$':0.05,
    #          'RP':0.2,
    #          'SYM':0,
    #          'TO':0.05,
    #          'UH':0.1}

    
def parseCommon(f, th, of, sof):
    o = open(of, 'w+')
    so = open(sof, 'w+')
    def scoreSen(sen, dic):
        sen = eval(sen)
        score = 0
        for wt in sen:
            if wt in dic:
                factor = weightDic[wt[1]]*1.0
                score += dic[wt]*factor/100
        return score
    all_hyps = [tgs for tgs in open(f)]
    num_sents = len(all_hyps) / 100
    all_list = []
    score_list = []
    answer_list = []
    hy_list = []

    for s in xrange(0, num_sents):
        hys = all_hyps[s*100 : (s+1)*100]
        keyset = set()
        common = {}
        for each in hys:
            lst = eval(each)
            for wordtag in lst:
                if wordtag in keyset:
                    common[wordtag] += 1
                else:
                    common[wordtag] = 1
                    keyset.add(wordtag)
        
        ls = [i for i in sorted(convert(common), key=itemgetter(1))[::-1] \
                  if i[0][1] in tags and i[1] > th]
        all_list += [ls]
        #loop again for scoring each hyp:
        senScore = []
        frqD = convertToDic(ls)
        for sen in hys:
            ss = scoreSen(sen, frqD)
            senScore += [ss]
            so.write("%s\n" % ss)

        maxindex = senScore.index(max(senScore))
        the_hy = hys[maxindex]
        score_list += [senScore]
        o.write("%s\n" % reassemble(the_hy))

    return 42


print parseCommon(infile, th_top, outfile, scoreout)
