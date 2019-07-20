import scrabble, qpAction
from scrabbleBoard import *
from MoveEncoding import *
from case import *

class Game:
    def __init__(self,players,racks,qpAction):
	self.qpAction = qpAction
        self.words = []
        self.lastword = ''
        self.passes = 0
        self.triesleft = 0
        self.rolls = []
        self.players = players
        self.myID = self.getID(qpAction.me)
        self.myRack = []
        #self.racks = []
        self.myRack = list(racks[self.myID])
        #for r in racks:
        #    self.racks.append(list(r))
        self.turn = 0
        if self.myID == None:
            #not playing
            self.gameOver()

	self.scrabble = scrabble.scrabble()
        self.board = self.scrabble.board
        #self.scrabble.board.clear()
        self.qpAction.newGameStarted()
        
    def changeTurn(self):
        self.turn = (self.turn + 1) % len(self.players)
    def isMyTurn(self):
        return self.myID == self.turn
    def doMove(self,playerAlias,encMove,newTiles=None):
        if self.board == None:
            print 'game.board not initialized'
            return
        playerID = self.getID(playerAlias)
        move = decodeMove(encMove,self.qpAction)
        self.board.doMove(move)
        letsUsed = getLettersUsed(encMove)
        if self.myID == playerID:
            for l in letsUsed:  #remove used letters from rack
		print "Game: doMove: letsUsed: "+l
                if islower(l):
                    self.myRack.remove(' ')
                else:
                    self.myRack.remove(l)
	    print 'extending myRack'
            self.myRack.extend(newTiles)    #add new letters to rack
    def play(self):
        if not self.isMyTurn():
            print 'its not my turn!'
            return
        myRack = ''.join(self.myRack)
        move = self.scrabble.getBestMove(myRack)
        if not move:
            print 'NO POSSIBLE MOVES, SWAP EM ALL! :-\\'
            if len(self.board) < (96 - 7 * len(self.players)):
		print "myRack is: "+myRack
                self.qpAction.swap(myRack)
            else:
                self.qpAction.giveUpTurn()
            return
        encMove = encodeMove(move[0],self)
        if not encMove:
            print 'all of',move,'is already on the board!!!!!!!'
            return
        self.qpAction.playMove(encMove)
    def badTry(self):
        pass
    def swap(self,alias,old,new):
	print "running swap in Game"
        playerID = self.getID(alias)
        if playerID == self.myID:
            for l in old:
		print "removing from rack: "+l
                self.myRack.remove(l)
	    print "appending to rack: "+new
            #self.myRack.append(new)
            self.myRack.extend(new)
    def getID(self,alias):
        playerID = None
        for i in range(len(self.players)):
            if self.players[i] == alias:
                playerID = i
                break
        return playerID
    def gameOver(self):
        self.board.clear()
