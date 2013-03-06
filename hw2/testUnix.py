import nltk
from nltk import *
import sys
import re
import shlex
import subprocess

# Read in a file and return a list of the file's lines
def readLines(filename):
    fh = open(filename, 'r')
    lines = fh.read().splitlines()
    fh.close
    return lines

# Call POS-tagger on a string
# Returns a list of tuples where each tuple consists of a word in the sentence
# and its corresponding part of speech. Punctuation has its own category.
def tagString(inp):
    pos = inp.lower() + '\n'
    j = 'java'
    mem = '-mx512m'
    pathFlag = '-classpath'
    jar = './stanford-postagger-full/stanford-postagger.jar'
    tagger = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
    mod = '-model'
    bidirect = './stanford-postagger-full/models/bidirectional-distsim-wsj-0-18.tagger'
    child = subprocess.Popen([j, mem, pathFlag, jar, tagger, mod, bidirect],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    newPos = child.communicate(pos)
    ret = newPos[0]
    ret = ret.rstrip('\r\n\r\n')
    ret = ret.rstrip('\n\n')
    ret = ret.split()
    retList = []
    for r in ret:
        w, p = r.split('_')
        retList.append( (w, p) )
    return retList

# Call POS-tagger on a file
def tagFile(infile, outfile):
    lines = readLines(infile)
    f = open(outfile, 'w')
    count = 0
    #outlines = []
    for line in lines:
        pos = tagString(line)
        #print pos
        f.write(str(pos)+ '\n')
        #outlines.append(pos)
        print '%d parsed' % count
        count += 1
    f.close()
    return 42

#print tagString('hello, my name is edward.')
testfile = 'data/test.hyp1-hyp2-ref'
trainfile = 'data/train.hyp1-hyp2-ref'

#print tagFile(trainfile)
taggedFile = 'taggedTrain.txt'
dicFile = 'dicTagged.txt'

testTag = 'testTagged.txt'

tempDic = {}

def processTagged(tf):
    # get test file dic
    f = open(tf, 'r')
    out = open('testTagged.txt', 'w')
    c = 0
    for line in f:
        if (c > 2):
            break
        (h1, h2, ref) = line.split('|||')
        h1 = h1.lower().strip()
        h2 = h2.lower().strip()
        ref = ref.lower().strip()

        if (h1 not in tempDic):
            posh1 = tagString(h1)
        else:
            posh1 = tempDic[h1]

        if (h2 not in tempDic):
            posh2 = tagString(h2)
        else:
            posh2 = tempDic[h2]
        if (ref not in tempDic):
            posref = tagString(ref) 

        out.write(h1 + '|||' + str(posh1) + '\n')
        out.write(h2 + '|||' + str(posh2) + '\n')
        out.write(ref + '|||' + str(posref) + '\n')
        c += 1
    out.close()
    f.close()
    return 42

processTagged(testfile)
#tagDic = {}
#def constructDic():
#    for line in open(testTag, 'r'):
#        print len(line.split('|||'))
#        #print line.split('|||')[1]
#        (key, pos) = line.split('|||')
#        tagDic[key] = pos
#constructDic()