import bisect
from binary_search import *
from case import *

class wordList:
    words = []
    letters = [[] for a in xrange(221)]
    rwords = []
    def loadList(words, rwords):
        print "!#!#!#!# LOADING LIST!!!!!!!!!!!!!!!"
        wordList.words = words
        wordList.rwords = rwords
        for w in words:
            for i,l in enumerate(w):
                wordList.letters[ord(l)].append((i, w))
   
    def letterCount(letter):
        if letter == ' ':
            return (2147483647, ' ')
        #return (len(wordList.letters[ord(letter)]), letter)
        try:
            return len(wordList.letters[ord(letter)])
        except:
            print ord(letter)
    
    def getShortestList(pattern):
        letter = min(map(wordList.letterCount, pattern))[1]
        return wordList.letters[ord(letter)]
    def startingWith(start,maxlen,bank):
        start = upper(start)
        words = wordList.words
        r = []
        bank = list(bank)
        i = bisect.bisect_left(words,start)
        lstart = len(start)
        lwords =  len(words)
        while i < lwords and words[i][:lstart] == start:
            if len(words[i]) <= maxlen:
#                if reduce(lambda x,y:x and y in bank,words[i],True):
#                    r.append(words[i])
                b = bank[:]
                w = words[i][:]
                for n,l in enumerate(w[lstart:]):
                    n += lstart
                    if l in b:
                        b.remove(l)
                    elif ' ' in b:
                        b.remove(' ')
                        w = w[:n] + lower(w[n]) + w[n+1:]
                    else:
                        break
                else:
                    r.append((w,b))
            i += 1
        return r
    def endingWith(end,maxlen,bank):
        end = upper(end)
        rend = wordList.reverseWord(end)
        rwords = wordList.rwords
        bank = list(bank)
        r = []
        i = bisect.bisect_left(rwords,rend)
        lrend = len(rend)
        lrwords =  len(rwords)
        while i < lrwords and rwords[i][:lrend] == rend:
            if len(rwords[i]) <= maxlen:
#                if reduce(lambda x,y:x and y in bank,rwords[i],True):
#                    r.append(rwords[i])
                b = bank[:]
                w = rwords[i][:]
                for n,l in enumerate(w[lrend:]):
                    n += lrend
                    if l in b:
                        b.remove(l)
                    elif ' ' in b:
                        b.remove(' ')
                        w = w[:n] + lower(w[n]) + w[n+1:]
                    else:
                        break
                else:
                    r.append((wordList.reverseWord(w),b))
            i += 1
        return r
    #matchingPattern preforms just as well even in cases where there is only one
    #    letter in the pattern, but in some cases (such as hangoffs) it is easier
    #    to just pass the letter, x, and max length if you don't have the pattern
    #    than to generate it, only to have it unpacked by matchingPattern
    def containingLetter(letter,x,maxlen,bank):
        words = wordList.letters[ord(upper(letter))]
        r = []
        endLets = maxlen - x
        bank = list(bank)
        for i, w in words:
            if i <= x and endLets >= len(w) - i:
                offset = x-i
                b = bank[:]
                for i,l in enumerate(w):
                    if i+offset != x:
                        if l in b:
                            b.remove(l)
                        elif ' ' in b:
                            b.remove(' ')
                            w = w[:i] + lower(w[i]) + w[i+1:]
                        else:
                            break
#                    elif l != letter:
#                        break
                else:
                    r.append((w,offset,b))
        return r
    def matchingPattern(pattern,bank):
        pattern = upper(pattern)
        letters = []
        blanks = []
        bank = list(bank)
        maxlen = len(pattern)
        for x, l in enumerate(pattern):
            if l != ' ':
                letters.append((l,x))
        #centerLet, center = min(map(lambda a: wordList.letterCount(a[0]) + (a[1],), letters))[1:]
        centerLet, center = min([(wordList.letterCount(a[0]),a[0],a[1]) for a in letters])[1:]
        letters.remove((centerLet, center))
        words = wordList.letters[ord(centerLet)]
        
        r = []
        endLets = maxlen - center
        for nwcenter, nw in words:
            if nwcenter <= center and endLets >= len(nw) - nwcenter:    #is word within proper range of length on either side of the 'center'?
                offset = center-nwcenter    #offset = how much shorter the head of the possible match is than the pattern
                for l,lx in letters:    #check if potential match matches the pattern specifed
                    #beautiful yet slightly slower version
                    #
                    #distFromCenter = lx - center
                    #nwlx = distFromCenter + nwcenter
                    #nwl = nw[nwlx]
                    #if nwlx < 0 or nwlx >= len(nw) or nwl != l:
                    #    break
                    
                    # same as above only condensed
                    nwlx = lx - offset  #nwlx = where the letter currently being tested should be on the potential match taking into consider the offset
                    if nwlx < 0 or nwlx >= len(nw): #if nwlx falls outside the bounderies of the potential match its not a match
                        break
                    nwl = nw[nwlx]
                    if nwl != l:    #if the letter in the appropriot location isn't the right one its not a match
                        break
                else:   #if it has all of the needed letters in the right places check if we can make it w/ our bank
                    b = bank[:]
                    for i,l in enumerate(nw):
                        if pattern[i+offset] == ' ':
                            if l in b:
                                b.remove(l)
                            elif ' ' in b:
                                b.remove(' ')
                                nw = nw[:i] + lower(nw[i]) + nw[i+1:]
                            else:
                                break
                    else:   #if it matches the pattern AND we can make it w/ our bank add it to r
                        r.append((nw,offset,b)) #r is a list of successful matches
                
        return r
    def allAreWords(possibleWords):
        for w in possibleWords:
            if binary_search(wordList.words,w) == -1:
                return False
        return True
    def reverseWord(w):
        rw = ""
        for i in xrange(len(w)-1,-1,-1):
            rw += w[i]
        return rw
            
    loadList = staticmethod(loadList)
    startingWith = staticmethod(startingWith)
    endingWith = staticmethod(endingWith)
    containingLetter = staticmethod(containingLetter)
    matchingPattern = staticmethod(matchingPattern)
    getShortestList = staticmethod(getShortestList)
    allAreWords = staticmethod(allAreWords)
    letterCount = staticmethod(letterCount)
    reverseWord = staticmethod(reverseWord)
