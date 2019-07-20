import stringtree, time, qpData
from User import *
from Game import *
from score import *
from types import *
from Table import *

log = open('gamelog.txt','a')
#l = open('raw.txt','a')

def event(line,qpAction):
    #l.write(line + '\n')
    #l.flush()
    info = line[0]
    flag = line[1]
    data = line[2:]
    if info == 'T':
        tableEvent(flag,data,qpAction)
    elif info == 'G':
        gameEvent(flag,data,qpAction)
    elif info == 'C':
        chatEvent(flag,data,qpAction)
    elif info == 'W':
        loginSuccess(line[1:],qpAction)
    elif info == 'A':
        print "I have no idea wtf this messege is for: " + line
    elif info == 'O':
        operationEvent(flag,data,qpAction)
    else:
        print "Weird message: " + info + flag + data
        
def tableEvent(flag,data,qpAction):
    #print "Table:", flag

    print "tableEvent with alias "+str(qpAction.me)
    if flag != 'I':
	print "test coming"
        alias = stringtree.head(data)
	print "alias: "+alias
        if qpAction.users.has_key(alias):
            table = getTable(alias,qpAction)
        else:
            table = None
    
    if flag == 'I':
        #recieve table info at initialization
	print "flag is I"
        st = stringtree.split(stringtree.split(data)[0])
        
        userst = stringtree.split(st[0])
        offlineuserst = stringtree.split(st[1])
        tablest = stringtree.split(st[2])
        tournamentst = stringtree.split(st[3])
        roomsettingst = st[4]
        freetable = None
        for user in userst:
            alias = stringtree.head(user)
            udata = stringtree.split(user)
            user = User(alias,udata[6],udata[1]) #new user
            qpAction.users[alias] = user

        for table in tablest:
            index = int(stringtree.head(table))
	    print "looping tables... "+str(index)+" ...qpAction.tables is now "+str(len(qpAction.tables))
            tablet = stringtree.split(table)
            tmembers = stringtree.split(tablet[0])
            tappliers = stringtree.split(tablet[1])
            tusers = stringtree.split(tablet[2])
            tsettings = tablet[3]
            gamestatus = int(tablet[4])

            if tmembers == []:
                freetable = index
                
            if len(qpAction.tables) == index:
                qpAction.tables.append(Table(index,tmembers,tappliers,tusers,tsettings,gamestatus,qpAction))
      
        print "freetable",freetable
        qpAction.initialized(freetable)

    elif flag == '+':
        #add user to list
        st = stringtree.split(data)[0]
        udata = stringtree.split(st)
        user = User(alias,udata[6],udata[1])
        user.alias = alias
        qpAction.users[alias] = user
    elif flag == '-':
	#print "removing", alias
	if qpAction.me == alias:
	    qpAction.startSame()
        #remove user from list
        if qpAction.users.has_key(alias):
            if table != None:
                if alias in table.members:
                    table.members.remove(alias)
                if alias in table.appliers:
                    table.appliers.remove(alias)
                if alias in table.users:
                    table.users.remove(alias)
            del qpAction.users[alias]
    elif flag == 'J':
        #user joined a table
        tableIndex = int(stringtree.split(data)[0])
        table = qpAction.tables[tableIndex]
        if table.addUser(alias):
            print "added", alias, "to table number", tableIndex
        if alias == qpAction.me:
	    print "!!! setting table to "+str(tableIndex)+" for alias "+qpAction.me
            qpAction.myTable = tableIndex
            if tableIndex == qpAction.applyingTo:
                qpAction.queue()
                qpAction.applyingTo = None
    elif flag == 'j':
        #user parted a table
        print 'removing', alias,'from table number',table.index
        if table and table.removeUser(alias):
            print 'removed', alias,'from table number',table.index
        if alias == qpAction.me:
            qpAction.myTable = None
    elif flag == 'Q':
        #user added to queue
        print "queue",alias,"to",table.index
        table.queueUser(alias)
        if table.index == qpAction.myTable and table.members[0] == qpAction.me: #this is happening to a table which i started?
          if len(table.members) + qpAction.acceptedusers < int(table.settings['players']): #there is an opening still in the table?
            #if qpAction.users[alias].rating > 1200:
                qpAction.acceptUser(alias)
                qpAction.acceptedusers += 1
    elif flag == 'q':
        #user removed from queue
        print "unqueue",alias,"to",table.index
        table.unqueueUser(alias)
    elif flag == 's':
        #table settings update
        settings = stringtree.split(data)[0]
        table.setSettings(settings)
        if alias == qpAction.waitPlayWith:
            qpAction.tryPlayWith(alias)
        elif alias == qpAction.me:
            if table.settings['players'] == '1':
                qpAction.startGame()
        else:
            if qpData.mode == '2':
                if table.settings['info'] == qpAction.wantrobotoinfo:
                    qpAction.tryPlayOnTable(table.index)
    elif flag == 'E':
        #end game
        if table:
            print "end game",table.index
            table.endGame()
            if table.index == qpAction.myTable:
		#added by olof: if game is nonetype, then somethings is wrong, so restart
		if type(qpAction.game) is NoneType:
			qpAction.startSame()
                for m in table.members:
                    if m != qpAction.me:
                        pass
                        #qpAction.privateChat(table.members[1],'Enjoy your game? Email me with comments, questions, or critiques at devilsadv@gmail.com')
                #qpAction.game.gameOver()
                qpAction.gameOver()
                log.flush()

		#added by olof to kill process at end of game
		#time.sleep(10)
		print "calling qpAction exit"
		qpAction.exit("end of game")

    elif flag == 'S':
        #start game
        print "start game ",table.index
        table.startGame()
        #if table.index == qpAction.myTable:
            #qpAction.newGameStarted()
        if qpAction.me in table.appliers:
            qpAction.gameOver()
    elif flag == 'A':
        applier = stringtree.split(data)[0]
        print alias,"accepts",applier,"to",table.index
        table.acceptUser(applier)
        if alias == qpAction.me: #i'm the acceptor?
            qpAction.acceptedusers -= 1
            if len(table.members) == int(table.settings['players']): #we now have all the players we need to start?
                qpAction.startGame()
                log.write('---------------NEW GAME---------------\n')
    elif flag == 'a':   
        table.nextApplier()
    else:
        print "Unknown Table:",flag, data
def gameEvent(flag,data,qpAction):
    print "Game:", flag,data
    log.write('G' + flag + data + '\n')
    if flag == 'W':
        #do move
        alias = stringtree.head(data)       #st[0] == encoded move #st[1] == not real words made #st[2] == new rack
        st = stringtree.split(data)         
        if alias == qpAction.me:
            if not st[1]:
                qpAction.game.doMove(alias,st[0],st[2])
            else:
                qpAction.game.badTry()
        else:
            if len(st) > 1:
                if not st[1]:
                    qpAction.game.doMove(alias,st[0])
                else:
                    qpAction.game.badTry()
            else:
                qpAction.game.doMove(alias,st[0])
                
    elif flag == 'N':
        #next player's turn
        qpAction.game.changeTurn()
        if qpAction.game.isMyTurn():
            qpAction.game.play()
        #print qpAction.game.board
    elif flag == 'P':
        #pass
        pass
    elif flag == 'g':
        #give up
        pass
    elif flag == 'C':
        #swap tiles
        alias = stringtree.head(data)
        st = stringtree.split(data)
	print "qpHandle: going to run qpAction.game.swap()"
        qpAction.game.swap(alias,st[0],st[1])
        
def chatEvent(flag,data,qpAction):
    print "Chat: ", flag,data
    alias = stringtree.head(data)
    msg = stringtree.head(stringtree.split(data)[1])
    if alias in qpAction.admins or alias == 'DevilsAdvocate':
        if msg[:8] == '!roboto ':
            qpAction.remoteAdmin(alias,msg[8:])
def loginSuccess(name,qpAction):
    print "Connected to quadplex server under username: " + name
    qpAction.me = name
def operationEvent(flag,data,qpAction):
    log.write('O' + flag + data + '\n')
    if flag == ':':
        print 'O' + flag + data
        st = stringtree.split(data)[0]
        #st = stringtree.split(st)
        gl = st.split('\x04')

        players = stringtree.split(gl.pop(0))
        if qpAction.me in players:
            tablesettings = gl.pop(0)
            del gl[0] #get rid of useless trash
            racks = [stringtree.split(gl.pop(0))[0] for i in players]
        
            if not qpAction.myTable: #if idk what table i'm on..
                #find out
                qpAction.myTable = [a for a in qpAction.tables if qpAction.me in a.members][0].index
            table = qpAction.tables[qpAction.myTable]

            #just in case to make sure the settings are right even though they should already be the same
            table.setSettings(tablesettings)
            #make sure the boardtype is set to the one we're playing on
            qpAction.boardtype = [a.split('=')[1] for a in tablesettings.split('&') if a.split('=')[0] == 'board'][0]
            
            #<trash>
            #qpAction.me = 'MrRoboto3'
            #</trash>
         
            print players,racks
            qpAction.game = Game(players,racks,qpAction)
            while gl:
                evnt = gl.pop(0)
                cmd = evnt[0]
                player = qpAction.game.players[qpAction.game.turn]
                if cmd == 'P':
                    pass
                elif cmd == 'C':
                    #swap
                    oldr, newr = stringtree.split(evnt)
                    qpAction.game.swap(player,oldr,newr)
                elif cmd == 'W':
                    #do move
                    move, badwords, newrack = stringtree.split(evnt)
                    if not badwords:
                        qpAction.game.doMove(player,move,newrack)
                    else:
                        qpAction.game.badTry()
                elif cmd == 'N':
                    qpAction.game.changeTurn()
                
            print qpAction.game.board
            if qpAction.game.isMyTurn():
                qpAction.game.play()
        else:
            qpAction.gameOver()
def getTable(alias,qpAction):
    return qpAction.tables[qpAction.users[alias].table]

