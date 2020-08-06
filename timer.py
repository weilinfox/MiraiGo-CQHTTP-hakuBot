from time import time, gmtime, strftime, sleep
from importlib import import_module
from hakuCore.config import INTERVAL
from quitAll import quitNow

def checkMsgLog():
    try:
        plgs = import_module('plugins.log')
    except:
        pass
    else:
        plgs.check()
    return

def getMsgRate():
    try:
        plgs = import_module('plugins.log')
    except:
        return 'Log plugin NOT found.'
    else:
        return str(plgs.msgRate())+'/min'

def main():
    while not quitNow():
        try:
            sleep(INTERVAL)
            checkMsgLog()
            print('\n[', strftime("%a, %m %b %Y %H:%M:%S GMT", gmtime()), '](速率):', getMsgRate())
        except:
            pass

    print("\nBye~ from timer")
