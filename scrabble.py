import sys, Patterns, qpData, time

from wordList import *
from scrabbleBoard import *
from binary_search import *
from score import *
from matchPattern import *
from case import *

#load language
words = open(qpData.dictfile,'r')
rwords = open(qpData.rdictfile,'r')
#words = map(lambda x: x[:-1],words)
words = [w.strip() for w in words]
#rwords = map(lambda x: x[:-1],rwords)
rwords = [w.strip() for w in rwords]
wordList.loadList(words,rwords)

class scrabble:
	def __init__(self):
		self.board = scrabbleBoard()
		self.board.clear()
	def getMoves(self,letters,useRack=True,verbose=False):
		pat = Patterns
		scoreW = scoreWord
		simpScore = simpleScore
		wList = wordList
		patterns = []
		if len(self.board):
			#board not blank
			rows = self.board.getrows()	
			for i, r in enumerate(rows):
				patterns.extend([(upper(a[0]),a[1],i,self.board.DIR_RIGHT) for a in pat.slice(r)])
			
			cols = self.board.getcols()
			for i, c in enumerate(cols):
				patterns.extend([(upper(a[0]),i,a[1],self.board.DIR_DOWN) for a in pat.slice(c)])
		else:
			#board is blank
			patterns.append(('        ',7,7,self.board.DIR_RIGHT))
		matches = []
		print "starting to think of patterns, length: "+str(len(patterns))
		then = time.time()
		for p in patterns:
			matches.extend(matchPattern(self.board,p,letters,verbose))
			used = time.time() - then
			if (used>10 and len(matches) > 0) or used>30:
				break
		print str(len(matches))+" patterns found"
		scores = []
		matches = [m for m in matches if wList.allAreWords(self.board.newWords(m))]
		for m in matches:
			newWords = self.board.newWords(m)
	#		if not wList.allAreWords(newWords):
			    #print 'foo'
	#                    matches.remove(m)
	#		else:
			if m[1] == 7 and m[2] == 7 and m[3] == self.board.DIR_RIGHT:
			    m = [m[0],7-len(m[0])/2,7,self.board.DIR_RIGHT]
			score = scoreW(self.board,m,letters,useRack)
			score += sum([simpScore(w) for w in newWords])
			scores.append(score)
		return matches, scores

	def getBestMove(self,letters,useRack=True,verbose=False):
		matches, scores = self.getMoves(letters,useRack,verbose)
		if not len(matches):
			return 0
		#highestscore = max(scores)
		m = zip(scores,matches)
		m.sort(None,None,True)
		dif = int(qpData.difficulty)
		if len(m) > dif:
		    score, move = m[dif]
		elif len(m) > 0:
		    print 'dont have that many results, doing worst'
		    score, move = m[-1]
		else:
		    return None
		return move, score
	def doBestMove(self,letters,useRack=True,verbose=False):
		m = self.getBestMove(letters,useRack,verbose)
		if m:
		    move,score = m
		    self.board.doMove(move)
		return m
