from scrabbleBoard import *
import qpData

import math
import cPickle
from case import *

#if qpData.boardtype == '0':
#elif qpData.boardtype == '1':
boardtypes = [
    #for when qpData.boardtype == 0
       ['T112111T111211T',
        '1D11131113111D1',
        '11D111212111D11',
        '211D1112111D112',
        '1111D11111D1111',
        '131113111311131',
        '112111212111211',
        'T112111D111211T',
        '112111212111211',
        '131113111311131',
        '1111D11111D1111',
        '211D1112111D112',
        '11D111212111D11',
        '1D11131113111D1',
        'T112111T111211T'],
    #for when qpData.boardtype == 1
       ['T1111T111T1111T',
        '1D1111D1D1111D1',
        '113111131111311',
        '111213111312111',
        '111111313111111',
        'T1131112111311T',
        '1D11311111311D1',
        '113112111211311',
        '1D11311111311D1',
        'T1131112111311T',
        '111111313111111',
        '111213111312111',
        '113111131111311',
        '1D1111D1D1111D1',
        'T1111T111T1111T']]
letterValues = []
rackValues = []
vowels = []
vowelValues = []
config = cPickle.load(file(qpData.scorepickle, 'r'))
letterValues = config['letterValues']
rackValues = config['rackValues']
vowels = config['vowels']
vowelValues = config['vowelValues']

"""
letterValues =[
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1,
    3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0]
rackValues =[
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 1, 1, 4, 1, 1, 2, 3, 0, 1, 2,
    1, 3, 1, 1, 4, 4, 6, 4, 2, 1, 1, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

vowels = ['A', 'E', 'I', 'O', 'U']
vowelValues = [0 , -2, -5, -10, -15, -17, -20]
"""

def scoreRackWithLookAhead(letters, draws):
    score = 0
    for draw in draws:
        score += scoreRack(letters + draw)
    score /= len(draws)

def scoreRack(letters):
    vowelCount = 0
    consonantCount = 0
    if len(letters) == 0:
        return 50
    if len(letters) > 7:
        letters = letters[:7]
    score = 0
    for i in xrange(len(letters)):
        score += rackValues[ord(letters[i])]
        if letters[i] in letters[:i]:
            score -= 5
        if letters[i] in vowels:
            vowelCount += 1
        elif letters[i] != ' ':
            consonantCount += 1
    score += vowelValues[int(math.fabs(vowelCount - consonantCount))]
    return score

        
        
def simpleScore(word):
    score = 0
    for letter in word:
        score += letterValues[ord(letter)]
    return score

"""
def scoreWord(gameBoard, move, rack,useRack = True, draws):
    word, x, y, direction = move
    letters = list(rack)
    score = 0
    mult = 1
    board = gameBoard.board
    startRack = rack
    for letter in word:
        if board[y][x] == ' ':
            if letter in letters:
                letters.remove(letter)
            else:
                letter = letter.lower()
                letters.remove(' ')
            if modifiers[y][x] == '1':
                score += letterValues[ord(letter)]
            elif modifiers[y][x] == '2':
                score += letterValues[ord(letter)] * 2
            elif modifiers[y][x] == '3':
                score += letterValues[ord(letter)] * 3
            elif modifiers[y][x] == 'T':
                score += letterValues[ord(letter)]
                mult *= 3
            else:
                score += letterValues[ord(letter)]
                mult *= 2
        else:
            score += letterValues[ord(letter)]
        if direction == 1:
            x += 1
        else:
            y += 1
    score = mult * score
    if len(startRack) == 7 and len(letters) == 0:
            score += 50
    if useRack:
        score +=  scoreRack(letters, draws)
        score +=  scoreRack(letters)
    return score
"""

def scoreWord(gameBoard, move, rack,useRack = True,):
    word, x, y, direction = move
    letters = list(rack)
    score = 0
    mult = 1
    board = gameBoard.board
    startRack = rack

    modifiers = boardtypes[int(qpData.boardtype)]
    
    for letter in word:
        if board[y][x] == ' ':
            if letter in letters:
                letters.remove(letter)
            elif ' ' in letters:
                letter = lower(letter)
                letters.remove(' ')
            else:
                print "wtf?!"
                print word, rack
                return -99999999
            if modifiers[y][x] == '1':
                score += letterValues[ord(letter)]
            elif modifiers[y][x] == '2':
                score += letterValues[ord(letter)] * 2
            elif modifiers[y][x] == '3':
                score += letterValues[ord(letter)] * 3
            elif modifiers[y][x] == 'T':
                score += letterValues[ord(letter)]
                mult *= 3
            else:
                score += letterValues[ord(letter)]
                mult *= 2
        else:
            score += letterValues[ord(letter)]
        if direction == 1:
            x += 1
        else:
            y += 1
    score = mult * score
    if len(startRack) == 7 and len(letters) == 0:
            score += 50
    if useRack:
        score +=  scoreRack(letters)
    return score
