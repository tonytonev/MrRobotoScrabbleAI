from binary_search import *
from case import *

class scrabbleBoard:
	def __init__(self):
		self.DIR_DOWN = 0
		self.DIR_RIGHT = 1
		self.board = []
		for i in range(15):
			self.board.append([' '] * 15)
	def __str__(self):
		s = ' _'*15 + '\n'
		for a in self.board:
			for b in a:
				s += '|' + (b == ' ' and '_' or b)
			s += '|\n'
		return s
	def __len__(self):
		return len(str.join('', [str.join('', i) for i in self.board]).replace(' ', ''))
		#reduce(lambda a, b: a + reduce(lambda x,y: x + int(y != ' '),b,0),self.board,0)
	def __getitem__(self,y):
		return self.board[y]
	def clear(self):
		self.__init__()
	def getrows(self):
		return map(lambda a: reduce(lambda x, y: x+y,a,""),self.board)
	def getcols(self):
		col = []
		for a in xrange(15):
			col.append([])
		for a in self.board:
			for i,b in enumerate(a):
				col[i].append(b)
						
		return map(lambda a: reduce(lambda x, y: x+y,a,""),col)
	def isLegal(self,move,words):
		word,x,y,direction = move
		word = upper(word)
		nwords = []
		if direction == self.DIR_RIGHT:
			if (x > 0 and self.board[y][x-1] != " " or x+len(word)-1 < 15 and self.board[y][x+len(word)-1]) != " ":
				return False
			for i, a in enumerate(word):
				if self.board[y][i+x] == " ":
					sword = y
					while sword > 0 and self.board[sword-1][x+i] != ' ':
						sword -= 1
					eword = y+1
					while eword < 15 and self.board[eword][x+i] != ' ':
						eword += 1
					if eword - sword > 1:
						nword = []
						for l in xrange(sword,eword):
							nword += self.board[l][x+i]
						nword[y-sword] = a
						nword = reduce(lambda x,y: x+y,nword,"")
						if binary_search(words,nword) == -1:
							return False
						nwords.append(nword)
				elif not self.board[y][i+x] == a:
					return False
				
		elif direction == self.DIR_DOWN:
			if (y > 0 and self.board[y-1][x] != " " or y+len(word) < 15 and self.board[y+len(word)][x]) != " ":
				return False
			for i, a in enumerate(word):
				if self.board[i+y][x] == " ":
					sword = x
					while sword > 0 and self.board[y+i][sword-1] != ' ':
						sword -= 1
					eword = x+1
					while eword < 15 and self.board[y+i][eword] != ' ':
						eword += 1
					if eword - sword > 1:
						nword = self.board[y+i][sword:eword]
						nword[x-sword] = a
						nword = reduce(lambda x,y: x+y,nword,"")
						if binary_search(words,nword) == -1:
							return False
						nwords.append(nword)
				elif not self.board[i+y][x] == a:
					return False
				
		else:
			return False
               
                return True, nwords
        
        def newWords(self,move):
        	word,x,y,direction = move
		word = word.upper()
		nwords = []
		if direction == self.DIR_RIGHT:
			for i, a in enumerate(word):
				if self.board[y][i+x] == " ":
					sword = y
					while sword > 0 and self.board[sword-1][x+i] != ' ':
						sword -= 1
					eword = y+1
					while eword < 15 and self.board[eword][x+i] != ' ':
						eword += 1
					if eword - sword > 1:
						nword = []
						for l in xrange(sword,eword):
							nword += self.board[l][x+i]
						nword[y-sword] = a
						nword = str.join('', nword)
						nwords.append(nword)
		elif direction == self.DIR_DOWN:
			for i, a in enumerate(word):
				if self.board[i+y][x] == " ":
					sword = x
					while sword > 0 and self.board[y+i][sword-1] != ' ':
						sword -= 1
					eword = x+1
					while eword < 15 and self.board[y+i][eword] != ' ':
						eword += 1
					if eword - sword > 1:
						nword = self.board[y+i][sword:eword]
						nword[x-sword] = a
						nword = str.join('', nword)
						nwords.append(nword)
		return nwords
    
	def doMove(self,move):
                word,x,y,direction = move
		if direction == self.DIR_RIGHT:
			self.board[y][x:x+len(word)] = word
		elif direction == self.DIR_DOWN:
			for i in xrange(len(word)):
				self.board[i+y][x] = word[i]
