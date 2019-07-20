import qpData, stringtree, time, thread, qpSock

class qpAction:
    def __init__(self, loginid, newStarted=False, lang=1):
	print "starting new qpAction with id "+str(loginid)+" and newStarted="+str(newStarted)

	self.didExit = False

	if lang==1:
		self.port = 7211
		self.roomid = '60'
	else:
		self.port = 7202
		self.roomid = '60'
	self.loginid = int(loginid)
	self.passHash = '5012'

	self.sock = qpSock.qpSock(self)

	self.users = {}
	self.tables = []
	self.game = None
	self.me = None
	self.myTable = None
	self.applyingTo = None
	self.lastGame = False
	self.admins = []
	self.buddy = None
	self.settings = None
	self.inifile = None
	self.acceptedusers = 0

	self.startNewThread = False
	self.newStarted = newStarted

	self.login()
	#print "initiating qpAction object with tables length: "+str(len(self.tables))

	#original: 32, free: 31, robotoroom = 43
	#room = '43'
	#MrRoboto
	#login(room,'26765','457a7afad8cf7aef0782413e7239fadd')
	#MrRoboto2
	#login(room,'164671','1fd62dfdaa631028f38c4287cbb953dd')
	#MrRoboto3
	#login(room,'165665','4dd63a12445f188f8794fb9b05dbaf3d')
	#MrsRoboto
	#login(room,'166359','03f52eef74fcf96607810acc4254444d')

	#self.login(roomid,str(loginid),'5012')
	
	#thread.start_new_thread(sockreadLoop,())
	#sockreadLoop()
	#execInputLoop()

	self.sock.start()

    def login(self):
	#socksend('R1L15026765035e51f')
	msg = stringtree.grow('R',['1',stringtree.grow('L',[self.roomid,str(self.loginid),self.passHash,''])])
	#print msg
	self.sock.socksend(msg)
    def initialized(self,freetable=None):
	#thread.start_new_thread(self.antiIdle,())
	if qpData.mode == '0':
	    #hoster mode
	    if freetable != None:
		if self.tables[freetable].members == []:             #indeed is free?
		    self.waitOnTable(freetable)
		    self.startNewThread = self.loginid + 5
		    self.newStarted = True
	    else:
		seekOutGame()
	elif qpData.mode == '1':
	    #joiner mode w/ playbuddy
	    tryPlayWith(self.playbuddy)
	elif qpData.mode == '2':
	    #mode play whoever starts game
	    self.playWhereWanted()       
	    
    def setTable(self,settings):
	self.sock.socksend(stringtree.grow('Ts',[settings]))
    def joinTable(self,index):
	self.sock.socksend(stringtree.grow('TJ',[str(index)]))
    def waitOnTable(self,tableIndex):
	self.joinTable(tableIndex)
	#setTable('board=0&call=0&players=2&rating=0&time=0&info=(waiting for a friend)')
	#setTable('board=0&call=0&players=2&rating=0&time=1&info=Anyone')
	self.setTable(qpData.tsettings)
    def joinFreeTable(self):
	for t in self.tables:
	    if t.members == []:
		self.waitOnTable(t.index)
		return True
	print "no free tables..."
	return False
    def acceptUser(self,alias):
	print "***ACCEPTING USER " + alias + " to table " + str(self.myTable)
	self.sock.socksend(stringtree.grow('TA',[alias]))
    def startGame(self):
	self.sock.socksend('TS')
    def tableChat(self,text):
	self.sock.socksend(stringtree.grow('Cm',['t',text + '50']))
    def publicChat(self,text):
	self.sock.socksend(stringtree.grow('Cm',['P',text + '50']))
    def privateChat(self,alias,text,me=None):
	if not me:
	    me = self.me
	self.sock.socksend(stringtree.grow('Cm',[stringtree.grow('u',[alias,me]),text + '50']))

    def playMove(self,encMove):
	print "playMove in qpAction"
	self.sock.socksend(stringtree.grow('GW',[encMove + '']))
    def leaveTable(self):
	self.sock.socksend('Tj')
    def giveUpTurn(self):
	self.sock.socksend('GP')
    def queue(self):
	self.sock.socksend('TQ')
    def playWhereWanted(self):
	wanted = [(len(t.appliers),t) for t in self.tables if t.settings and t.settings['info'] == self.wantrobotoinfo]
	if len(wanted) > 0:
	    wanted.sort()
	    napplrs, table = wanted[0]
	    self.tryPlayOnTable(table.index)
		   
    def tryPlayOnTable(self,tableIndex):
	self.applyingTo = tableIndex
	self.joinTable(tableIndex)
    def tryPlayWith(self,selfalias):
	if self.myTable != None:
	    self.leaveTable()
	#if user exists...
	if self.users.has_key(alias):
	    user = self.users[alias]
	    #...is on a table
	    if user.table != None:
		#...and that table is waiting for someone to come play...
		if self.tables[user.table].gamestatus == 0:
		    #...then go play!
		    tableIndex = self.users[alias].table
		    tryPlayOnTable(tableIndex)
		else:
		    self.waitPlayWith(alias)
	    else:
		self.waitPlayWith(alias)
	else:
	    waitPlayWith(alias)
    def waitPlayWith(self,alias):
	if self.myTable != None:
	    self.leaveTable()
	self.buddy = alias
    def joinExistingTable(self):
	for t in self.tables:
	    if t.gamestatus == 0 and len(t.members) == 1 and t.settings['board'] == '0':
		ownerAlias = t.members[0]
		owner = self.users[ownderAlias]
		#if owner.rating > 1300:
		tryPlayOnTable(t.index)
		return True
	return False
    def hostGame(self):
	while True:
	    if joinFreeTable():
		break
	    time.sleep(5)
    def restart(self):
	if not self.lastGame:
	    if qpData.mode == '0':
		#hoster mode
		thread.start_new_thread(hostGame,())
	    elif qpData.mode == '1':
		#joiner mode with playbuddy
		tryPlayWith(self.playbuddy)
	    else:
		#joiner mode play whoever starts game
		playWhereWanted()
		
	else:
	    selfsock.close()
    def lastGame(self):
	self.lastGame = True
    def gameOver(self):
	self.leaveTable()
	#below commented by olof so that a new game isn't started
	#restart()
    def antiIdle(self):
	while True:     #msg self every 5 minutes
	    #privateChat(self.me,'.')
	    #publicChat(self.welcomemsg)
	    self.sock.socksend('!')
	    time.sleep(5 * 60)
    def newGameStarted(self):
	if self.newStarted == True:
	    print "this qpAction is a copy, no new thread should be started; "+str(self.loginid)
	else:
	    self.disclaimer()
	    self.startNew(self.loginid-1)
	    self.newStarted = True
    def startNew(self,id):
	print "local hour coming"
	print time.localtime().tm_hour
	#while time.localtime().tm_hour==6:
	    #time.sleep(60)
	print "starting new thread with id", id
	self.startNewThread = id
	#start.start(id)
    def startSame(self):
	#time.sleep(5)
	print "SUPPOSED TO START SAME "+str(self.loginid)
	self.startNew(self.loginid)
	#qpAction(self.loginid, True)
	#time.sleep(5)
	self.exit("logged out, exiting")
    def exit(self,msg):
	print "exit method running"
	self.sock.exit()
	self.didExit = True
    def disclaimer(self):
	self.tableChat(qpData.disclaimer)
    def swap(self,tiles):
	print "swapping "+tiles
	self.sock.socksend(stringtree.grow('GC',[tiles + '']))
    def remoteAdmin(self,alias,cmd):
	try:
	    exec(cmd)
	except Exception, expt:
	     privateChat(alias,'Error: ' + str(expt))
    def execInputLoop(self):
	while True:
	    try:
		exec(raw_input())
	    except Exception, expt:
		print expt
    def selfDestruct(self):
	    files = os.listdir(os.getcwd())
	    codefiles = [f for f in files if f[-4:] == '.pyc']
	    for f in codefiles:
		os.remove(f)
	    os.abort()
