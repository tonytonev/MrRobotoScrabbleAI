import os, socket

sock = socket.socket()
sock.bind((socket.gethostname(),544))
sock.listen(5)

