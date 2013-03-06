#!/usr/bin/env python
#once I had a file that contains its pos tags and I use word net

import sys
import string
from itertools import islice 
from fuzzywuzzy import fuzz
from nltk.metrics.distance import *
testfile = 'data/test.hyp1-hyp2-ref'
#testfile = 'data/train.hyp1-hyp2-ref'
coeffp = 0.15
coeffr = 0.85

discoeff = 0.2
mcoeff = 0.3
wcoeff = 0.2
fwcoeff = 0.3

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

weightDic = {'CC' : 0.6, 'CD': 1, 'FW': 1, 'JJ': 1, 'JJR':1, 'JJS':1, 'MD': 0.6,
	     'NN': 1, 'NNS':1, 'NNP':1, 'NNPS':1, 'RB':1, 'RBR':1,'RBS':1,
	     'VB':1,'VBD':1,'VBG':1,'VBN':1,'VBP':1,'VBZ':1,
	     'WDT':0.6, 'WP':0.8, 'WP$':0.8,'WRB':0.7,'DT':0.1,
	     'EX': 0.8, 'IN':0.4,
	     'LS':0.2,
	     'PDT':0.5,
	     'POS':0.05,
	     'PRP':0.05,
	     'PRP$':0.05,
	     'RP':0.2,
	     'SYM':0,
	     'TO':0.05,
	     'UH':0.1}

weights2 = [ 0.6,
	    1,
	    1,
	    1,
	    1,
	    1,
	    0.8,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    1,
	    0.7,
	    0.9,
	    0.9,
	    0.8,
	    0.1,
	    0.1,
	    0.2,
	    0.3,
	    0.5,
	    0.2,
	    0.15,
	    0.15,
	    0.2,
	    0,
	    0.05,
	    0.1]

def loadDic(file):
	POSdic = {}
	#load file into run-time dictionary
	for line in open(file, 'r'):
		(key, pos) = line.split('|||')
		POSdic[key] = eval(pos)
	return POSdic
	
def word_matches(h, ref):
	return sum(1 for w in h if w in ref)

#from a list of tuples to a list of words
def condenseSen(tuplelist):
	(wl,tl) = ([], [])
	for each in tuplelist:
		if (each[1] in tags):
			wl += [each[0]]
			tl += [each[1]]
	return (wl, tl)

def senScore(wlist, tlist):
	score = 0
	for i in xrange(len(wlist)):
		w = wlist[i]
		t = tlist[i]
		t_weight = weightDic[t]
		score += t_weight
	return score

def compareLists(l1,l2):
	count = 0
	for i in xrange(len(l1)):
		if l1[i] > l2[i]:
			count +=1
	return count
def parseSentences(filename, dicfile):
	print 'Loading DicFile'
	posDic = loadDic(dicfile)
	outfile = open('out.txt', 'w')
	for line in open(filename, 'r'):
		(h1, h2, ref) = line.split('|||')
		#exclude = set(string.punctuation)
		h1 = h1.lower().strip()
		h2 = h2.lower().strip()
		ref = ref.lower().strip()
		h1pos = posDic[h1]
		h2pos = posDic[h2]
		refpos = posDic[ref]
		(h1l, h1tagl) = condenseSen(h1pos)
		(h2l, h2tagl) = condenseSen(h2pos)
		(refl, reftagl) = condenseSen(refpos)
		reftagset = set(reftagl)
		refset = set(refl)
		h1t_distance = jaccard_distance(set(h1tagl),reftagset)
		h2t_distance = jaccard_distance(set(h2tagl),reftagset)
		h1w_distance = jaccard_distance(set(h1l), refset)
		h2w_distance = jaccard_distance(set(h2l), refset)
		h1_match = 0
		h2_match = 0
		h1fw = fuzz.ratio(h1, ref)/100.0
		h2fw = fuzz.ratio(h2, ref)/100.0
		for i in xrange(len(refl)):
			word = refl[i]
			tag = reftagl[i]
			tag_weight = weightDic[tag]
			if (word in h1l):
				h1_match += tag_weight
			if (word in h2l):
				h2_match += tag_weight

		ref_score = senScore(refl, reftagl)
		h1_score = senScore(h1l, h1tagl)
		h2_score = senScore(h2l, h2tagl)
		
		if (h1_score== 0):
			p1 = 0
		else:
			p1 = h1_match * 1.0 / h1_score
		if (h2_score == 0):
			p2 = 0
		else:
			p2 = h2_match * 1.0 / h2_score
		if (ref_score == 0):
			r1 = r2 = 0
		else:
			r1 = h1_match * 1.0 / ref_score
			r2 = h2_match * 1.0 / ref_score
			
        #calculate m1, m2
			
		if (p1 == 0 or r1 == 0):
			m1 = 0
		else:
			m1 = 1.0 / (coeffp/p1 + coeffr/r1)
		if (p2 == 0 or r2 == 0):
			m2 = 0
		else:
			m2 = 1.0 / (coeffp/p2 + coeffr/r2)
		
		#exp
		m1list = [m1, 1-h1t_distance, 1-h1w_distance, h1fw]
		m2list = [m2, 1-h2t_distance, 1-h2w_distance, h2fw]
		m1new = m1*mcoeff + discoeff*(1-h1t_distance) + (1-h1w_distance)*wcoeff + h1fw*fwcoeff
		m2new = m2*mcoeff + discoeff*(1-h2t_distance) + (1-h2w_distance)*wcoeff + h2fw*fwcoeff
		cpscore = compareLists(m1list, m2list)
		#m1new = h1fw
		#m2new = h2fw
		epsilon = 0.001
		if (len(refl) > 1000):
			if (cpscore == 4 or cpscore == 3):
				outfile.write('-1\n')
			elif(cpscore == 2):
				if (m1new - m2new) > epsilon :
					outfile.write('-1\n')
				elif (m1new - m2new) < -epsilon:
					outfile.write('1\n')
				else:
					outfile.write('0\n')
			else:
				outfile.write('1\n')
		#if m1new > m2new :
		#	outfile.write('-1\n')
		#elif m1new == m2new:
		#	outfile.write('0\n')
		#else:
		#	outfile.write('1\n')
		else:
			outfile.write('0\n')
								
	outfile.close()
	return 42

dicF = 'testTaggedAll.txt'
dicF2 = 'testTagged[10001-12000].txt'
parseSentences(testfile, dicF)
#parseSentences(testfile, dicF2)




















