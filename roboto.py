# -*- coding: iso-8859-15 -*-
import qpData, sys

if len(sys.argv) > 1:
	lang = int(sys.argv[1])
else:
	lang = 1

if lang == 1:
	qpData.scorepickle = "lang/swedishRacks1.tvl"
	qpData.dictfile = "lang/swedish.txt"
	qpData.rdictfile = "lang/swedish.reverse.txt"
	info = "Vill du möta en robot?"
	qpData.disclaimer = "Du spelar just nu mot en robot och inte en annan person. Om du föredrar att spela mot en mänsklig motståndare, avsluta spelet nu genom att klicka på Ge upp. Om du avslutar nu kommer spelet inte att räknas. I annat fall, hoppas att spelet blir trevligt och lycka till!"
else:
	qpData.scorepickle = "lang/englishRacks1.tvl"
	qpData.dictfile = "lang/english.txt"
	qpData.rdictfile = "lang/english.reverse.txt"
	info = "Want to play a robot?"
	qpData.disclaimer = "You are playing against a robot and NOT another person. If you prefer to play against a human being, close now by clicking Give up. If you close it now, the game will not count. Otherwise, enjoy your game and good luck!"

qpData.boardtype = '0'
qpData.difficulty = '0'
qpData.mode = '0'
qpData.tsettings = 'board='+qpData.boardtype+'&call=0&players=2&rating=0&time=1&info='+info

print qpData.scorepickle
#qpData.inifile = 'MrRoboto.ini'

import qpAction, time

threads = []

def getThread(n, newStarted=False):
        q = qpAction.qpAction(n, newStarted, lang)
	return q

threads.append(getThread(-1))

while 1:
	for i, t in enumerate(threads):
		new = t.startNewThread
		if new != False:
			threads.append(getThread(new, new == t.loginid and t.newStarted))
			qpData.mode = (set(['0', '2']) - set(qpData.mode)).pop()
		t.startNewThread = False
		if t.didExit == True:
			print "now popping thread with id "+str(t.loginid)
			threads.pop(i)
	time.sleep(1)

#start.start(-1)
