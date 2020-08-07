from time import time, gmtime, strftime, sleep
from importlib import import_module
from hakuCore.config import INTERVAL
from hakuCore.logging import printLog
from quitAll import quitNow
import hakuCore.timeEvent

def checkMsgLog():
    try:
        plgs = import_module('plugins.log')
    except:
        printLog('INFO', 'timer.py: log plugin NOT found')
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
    pmsgr = '-1/min'
    nmsgr = '0/min'
    while not quitNow():
        try:
            #hakuCore.timeEvent.main()
            sleep(INTERVAL)
            checkMsgLog()
            nmsgr = getMsgRate()
            if pmsgr != nmsgr or nmsgr != '0/min':
                print('\n[', strftime("%a, %m %b %Y %H:%M:%S GMT", gmtime()), '](速率):', nmsgr)
            pmsgr = nmsgr
        except:
            printLog('ERROR', 'timer.py: in main loop')

    print("\nBye~ from timer")
