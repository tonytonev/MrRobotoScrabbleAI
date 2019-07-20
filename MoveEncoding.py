def decodeMove(qpEncoded,qpAction):
    x = ord(qpEncoded[0]) -65
    y = ord(qpEncoded[1]) -65
    word = ''
    if qpEncoded[0] == qpEncoded[-3]: #if first and last x are the same
        dir = 0                           #direction is down otherwise right
	ly = y
	for l in range(2,len(qpEncoded),3):
		ty = ord(qpEncoded[l-1])-65
		for i in range(1,ty-ly):    #if there is a gap between last y
		    word += qpAction.game.board[ly+i][x]         #and this y put in letter in board
		word += qpEncoded[l]
		ly = ty
    else:
	dir = 1
	lx = x
	for l in range(2,len(qpEncoded),3): #same w/ x
		tx = ord(qpEncoded[l-2])-65
		for i in range(1,tx-lx):
                    word += qpAction.game.board[y][lx+i]
		word += qpEncoded[l]
		lx = tx
    return (word,x,y,dir)

def encodeMove(move,game):
    word,x,y,dir = move
    encoded = ''
    if dir == 0: #if down
        for i in range(len(word)):
            if game.board[y+i][x] == ' ':
                encoded += chr(x+65) + chr(y+i+65) + word[i]
    else:        #if right
        for i in range(len(word)):
            if game.board[y][x+i] == ' ':
                encoded += chr(x+i+65) + chr(y+65) + word[i]
    return encoded

def getLettersUsed(qpEncoded):
    lets = []
    for i in range(2,len(qpEncoded),3):
        lets.append(qpEncoded[i])
    return lets
