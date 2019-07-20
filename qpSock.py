import socket, qpHandle
from threading import Thread

class qpSock(Thread):
    def __init__(self,qpAction):
	Thread.__init__(self)
	self.doExit = False
	self.qpAction = qpAction
	self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('quadplex.com', qpAction.port))
    def run(self):
	sock = self.sock
	readbuffer = ""
	sock.settimeout(None)
	while self.doExit == False:
	    print "running socket with "+str(self.qpAction.loginid)
	    try:
		    newdata = sock.recv(4096)
	    except socket.error:
		    print "socket error with "+str(self.qpAction.loginid)
		    self.qpAction.startSame()
	    print "reading:", newdata
	    if len(newdata) == 0:
		    self.qpAction.startSame()
	    readbuffer += newdata
	    if "\n" in newdata:
		lines = readbuffer.splitlines()
		if len(lines) > 1:
		    if readbuffer[-1] != '\n':
			for l in lines[:-1]:
			    qpHandle.event(l,self.qpAction)
			readbuffer = lines[-1]
		    else:
			for l in lines:
			    qpHandle.event(l,self.qpAction)
			readbuffer = ""
		else:
		    print "###qpSock 40: "+str(self.qpAction.loginid)+" | "+lines[0]
		    qpHandle.event(lines[0],self.qpAction)
		    readbuffer = ""
	print "#########################closing socket!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print ".............................."
	self.sock.close()
	return
    def socksend(self,msg):
	    sock = self.sock
	    try:
		msg += '\n'
		while msg:
		    print "socksend with " + str(self.qpAction.loginid) + ": "+msg
		    sentlen = sock.send(msg)
		    msg = msg[sentlen:]
	    except socket.error:
		    print "socket send error"
		    self.qpAction.startSame()
    def exit(self):
	print "running exit in qpSock"
	self.doExit = True
