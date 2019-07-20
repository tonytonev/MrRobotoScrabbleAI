import connect

def start(id):
    c = connect.connect(str(id))
    #c.setDaemon(True)
    c.start()
