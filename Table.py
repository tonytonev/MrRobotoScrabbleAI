class Table:
    def __init__(self,index,members,appliers,users,settings,gamestatus,qpAction):
        self.index = index
        self.members = members
        self.appliers = appliers
        self.users = users
        self.settings = {}
        self.setSettings(settings)
        self.gamestatus = gamestatus #game ended if > 1, game started if == 1, game not started if == 0
	self.qpAction = qpAction
	print "creating Table object with "+str(self.qpAction.me)
    def setSettings(self,settings):
        props = settings.split('&')
        for p in props:
            s = p.split('=')
            if len(s) > 1 and s[0] and s[1]:
                self.settings[s[0]] = s[1]
    def addUser(self,userAlias):
	print "running addUser with "+self.qpAction.me
        user = self.qpAction.users[userAlias]
        if userAlias in self.users:
            print "can't join", userAlias, 'already in this table!'
            return False
        if user.table > -1 and user.table != self.index:
            print "can't join", self.index,", ", userAlias, 'is already on table', user.table
            return False
        user.table = self.index
        self.users.append(userAlias)
        if len(self.members) == 0 :
            self.members.append(userAlias)
        return True
    def removeUser(self,userAlias):
        user = self.qpAction.users[userAlias]
        if not userAlias in self.users:
            print userAlias, 'not in table!'
            return False
        try:
            self.appliers.remove(userAlias)
        except:
            pass
        try:
            self.users.remove(userAlias)
        except:
            pass
        try:
            self.members.remove(userAlias)
        except:
            pass
        user.table = -1
        self.check()
        return True
    def queueUser(self,alias):
        if alias not in self.users:
            print alias, "can't join queue, not user"
            return False
        if self.gamestatus == 1:
            print alias, "can't join queue, game has started", self.index
            return False
        if not self.settings:
            print alias, "can't join queue, settings not set"
            return False
        if alias in self.appliers:
            print alias, "can't join queue, already in it"
            return False
        self.appliers.append(alias)
        return True
    def unqueueUser(self,alias):
        try:
            self.appliers.remove(alias)
            return True
        except:
            return False
            
    def check(self):
        print "checking",self.index,"...",
        if self.gamestatus > 1 and self.allMembersGone():
            self.members = []
        if not self.members:
            self.settings = {}
            self.gamestatus = 0
            if self.appliers:
                self.members.append(self.appliers[0])
                del self.appliers[0]
        if not self.members and self.users:
            self.members.append(self.users[0])
            
        print "status", self.gamestatus
    def allMembersGone(self):
        for m in self.members:
            if m in self.users:
                return False
        return True
    def endGame(self):
        self.gamestatus = 2
        self.check()
    def startGame(self):
        if not self.settings or not self.settings.has_key('players') or len(self.members) != int(self.settings['players']) or self.gamestatus == 1:
	    #rest of print commented out by olof, gave error
            print "can't start game, table not ready"#, self.index, self.settings == None, len(self.members) != int(self.settings['players']) ,self.gamestatus == 1
	    self.qpAction.startSame()
        self.appliers = []
        self.gameStatus = 1
    def acceptUser(self,applierAlias):
        if self.gamestatus != 1:
            try:
                self.appliers.remove(applierAlias)
            except:
                print "can't accept user",applierAlias,'to table',self.index,'; not applier (doing it anyway)'
                if applierAlias not in self.users:
                    self.users.append(applierAlias)
            self.members.append(applierAlias)
    def nextApplier(self):
        if self.appliers:
            reject= self.appliers[0]
            del self.appliers[0]
            self.appliers.append(reject)
