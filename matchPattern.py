#import re
#from regexmatch import *
from wordList import *

def isPossible(board,move,letters):
    lets = letters[:]
    word, x, y, dir = move
    if dir == board.DIR_RIGHT:
        if x + len(word) > 15: return False
    else:
        if y + len(word) > 15: return False

    for i, a in enumerate(word):
        if dir == board.DIR_RIGHT:
            l = board[y][x+i]
        else:
            l = board[y+i][x]
        if l == ' ':
            if a in lets:
                lets.remove(a)
            elif ' ' in lets:
                move[0] = word[:i] + lower(a) + word[i+1:]
                lets.remove(' ')
            else:
                return False
    if len(lets) == len(letters):
        #print str(board)
        #print letters
        #print x, y, dir, word
        return False
    return True

def matchPattern(board,patinfo,bank,verbose=False):
    pattern, px, py, pdir = patinfo
    if pattern.count(" ") == 0:
        return []
    bank = bank.upper()
    spattern = pattern.strip()
    innerBlanks = spattern.count(" ") > 0
    leadingSpaces = pattern.find(spattern)
    trailingSpaces = len(pattern) - leadingSpaces - len(spattern)
    matches = []
    srchAlg = ''
    if verbose: print pattern
    if not leadingSpaces and not innerBlanks:
        srchAlg = 'startingWith'
        words = wordList.startingWith(spattern,len(pattern),bank)
        for w,rbank in words:
            if w != spattern:
                move = [w,px,py,pdir]
                if len(w) == len(spattern) + 1:
                    srchAlg += ',getHangOffs'
                    lindex = len(spattern)
                    hangoffs = getHangOffs(board,move,lindex,rbank)
                    for h in hangoffs:
                        matches.append(h)
                elif len(w) > len(spattern):
                    matches.append(move)
    elif not trailingSpaces and not innerBlanks:
        srchAlg = 'endingWith'
        #print 'wordList.endingWith(' + spattern + ',' + str(len(pattern)) + ',' + bank +')'
        words = wordList.endingWith(spattern,len(pattern),bank)
        for w,rbank in words:
            if w != spattern:
                offset = len(pattern) - len(w)
                if pdir == board.DIR_RIGHT:
                    move = [w,px+offset,py,pdir]
                else:
                    move = [w,px,py+offset,pdir]
                
                if len(w) == len(spattern) + 1:
                    srchAlg += ',getHangOffs'
                    lindex = 0
                    #print "getHangOffs(board,",move,",",lindex,',',rbank,')'
                    hangoffs = getHangOffs(board,move,lindex,rbank)
                    for h in hangoffs:
                        matches.append(h)
                elif len(w) > len(spattern):
                    matches.append(move)
    else:
        srchAlg = 'matchingPattern'
        words = wordList.matchingPattern(pattern,bank)
        for w, offset,rbank in words:
            if pdir == board.DIR_RIGHT:
                move = [w,px+offset,py,pdir]
            else:
                move = [w,px,py+offset,pdir]
            if not innerBlanks and len(w) == len(spattern)+1:
                srchAlg += ',getHangOffs'
                lindex = int(not w.find(spattern)) * len(spattern)
                hangoffs = getHangOffs(board,move,lindex,rbank)
                for h in hangoffs:
                    matches.append(h)
            elif innerBlanks or len(w) > len(spattern):
                matches.append(move)
    #else:
    #    print 'reMatch'
    #    matches = reMatch(board,patinfo,bank)
    
    if verbose: print patinfo,srchAlg
    banklist = list(bank)
    #print banklist
    for m in matches[:]:
        if not isPossible(board,m,banklist):
            print m, 'is not possible!',bank,patinfo, 'used:',srchAlg
            matches.remove(m)
    return matches
    
def getHangOffs(board,move,hlindex,bank):
    word, x, y, dir = move
    #print move
    hletter = word[hlindex]
    #find out how far the hangoff can extend in either direction and make a pattern form that
    if dir == board.DIR_RIGHT:
        x += hlindex
        if (y > 0 and board[y-1][x] != ' ') or (y < 14 and board[y+1][x] != ' '):
            return [move]
        spat = y
        while spat > 0 and board[max(spat-2,0)][x] == ' ':
            spat -= 1
        epat = y+1
        while epat < 15 and board[min(epat+1,14)][x] == ' ':
            epat += 1
        hletterLoc = y-spat
    else:
        y += hlindex
        if x > 0 and board[y][x-1] != ' ' or x < 14 and board[y][x+1] != ' ':
            return [move]
        spat = x
        while spat > 0 and board[y][max(spat-2,0)] == ' ':
            spat -= 1
        epat = x+1
        while epat < 15 and board[y][min(epat+1,14)] == ' ':
            epat += 1
        hletterLoc = x-spat
    hpatLen = epat - spat
    if hpatLen <= 1:
        return [move]
    
    hangoffs = []
    hdir = int(not dir)
    if hletterLoc == 0:
        words = wordList.startingWith(hletter,hpatLen,bank)
        for w,rbank in words:
            hmove = [w,x,y,hdir]
            hangoffs.append(hmove)
    elif hletterLoc == hpatLen - 1:
        words = wordList.endingWith(hletter,hpatLen,bank)
        for w,rbank in words:
            offset = hpatLen - len(w)
            if hdir == board.DIR_RIGHT:
                hmove = [w,spat+offset,y,hdir]
            else:
                hmove = [w,x,spat+offset,hdir]
            hangoffs.append(hmove)
    else:
        words = wordList.containingLetter(hletter,hletterLoc,hpatLen,bank)
        for w, offset,rbank in words:
            if hdir == board.DIR_RIGHT:
                hmove = [w,spat+offset,y,hdir]
            else:
                hmove = [w,x,spat+offset,hdir]
            hangoffs.append(hmove)
    return hangoffs or [move]
