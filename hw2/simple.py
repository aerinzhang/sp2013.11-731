#!/usr/bin/env python
import sys
import string
from itertools import islice 

testfile = 'data/test.hyp1-hyp2-ref'
#testfile = 'data/train.hyp1-hyp2-ref'
coeffp = 0.05
coeffr = 0.95

def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

def parseSentences(filename):
    outfile = open('out.txt', 'w')
    # from evaluate by Chris
    #def sentences():
    #    with open(filename) as f:
    #        for pair in f:
    #            yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
                
    #for h1l, h2l, nref in islice(sentences(), None):
    for line in open(filename, 'r'):
        (h1, h2, ref) = line.split('|||')
        exclude = set(string.punctuation)                                                                                                                               
        #nh1 = ''.join(ch for ch in h1 if ch not in exclude)
        #nh2 = ''.join(ch for ch in h2 if ch not in exclude)
        #nref = ''.join(ch for ch in ref if ch not in exclude)
        #rset = set(nref.split())
        #rset = set(nref)
        h1l = h1.lower().split()
        h2l = h2.lower().split()
        refl = ref.lower().split()
        
        #h1_match = word_matches(h1l, rset)
        #h2_match = word_matches(h2l, rset)
        #print(-1 if h1_match > h2_match else # \begin{cases}                                 
        #       (0 if h1_match == h2_match
        #        else 1)) # \end{cases}                  
        h1_match = 0
        h2_match = 0
        for each in refl:
            if each in h1l:
                h1_match += 1
            if each in h2l:
                h2_match += 1

        #length = len(nref)
        length = len(refl)
        if (len(h1l) == 0):
            p1 = 0
        else:
            p1 = h1_match * 1.0 / len(h1l)
        if (len(h2l) == 0):
            p2 = 0
        else:
            p2 = h2_match * 1.0 / len(h2l)
        if (length == 0):
            r1 = r2 = 0
        else:
            r1 = h1_match * 1.0 / length
            r2 = h2_match * 1.0 / length

        #calculate m1, m2

        if (p1 == 0 or r1 == 0):
            m1 = 0
        else:
            m1 = 1.0 / (coeffp/p1 + coeffr/r1)
        if (p2 == 0 or r2 == 0):
            m2 = 0
        else:
            m2 = 1.0 / (coeffp/p2 + coeffr/r2)
        if m1 > m2 :
            outfile.write('-1\n')
        elif m1 == m2:
            outfile.write('0\n')
        else:
            outfile.write('1\n')
    outfile.close()
    return 42



parseSentences(testfile)
