# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from time import sleep
from importlib import import_module
from hakuCore.config import INTERVAL
from quitAll import quitNow
from hakuCore.hakuCore import hakuTime
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
    hakuCore.timeEvent.load()
    while not quitNow():
        try:
            sleep(INTERVAL)
            checkMsgLog()
            # 打印小白流量
            nmsgr = getMsgRate()
            if pmsgr != nmsgr or nmsgr != '0/min':
                hakuCore.logging.printLog('速率', nmsgr)
            pmsgr = nmsgr
            # 触发时间事件
            hakuTime()
        except:
            hakuCore.logging.printLog('ERROR', 'timer.py: in main loop')

    hakuCore.logging.directPrintLog("\nBye~ from timer")
