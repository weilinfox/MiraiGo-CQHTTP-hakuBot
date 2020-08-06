
quitThread = False

def quitNow():
    global quitThread
    return quitThread

def setQuit():
    global quitThread
    quitThread = True
