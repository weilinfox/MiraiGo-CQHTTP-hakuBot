from time import sleep
from importlib import import_module
from hakuCore.config import INTERVAL
from quitAll import quitNow
import hakuCore.timeEvent
import hakuCore.logging

def checkMsgLog():
    try:
        plgs = import_module('plugins.log')
    except:
        hakuCore.logging.printLog('INFO', 'timer.py: log plugin NOT found')
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
                hakuCore.logging.printLog('速率', nmsgr)
            pmsgr = nmsgr
        except:
            hakuCore.logging.printLog('ERROR', 'timer.py: in main loop')

    hakuCore.logging.directPrintLog("\nBye~ from timer")
