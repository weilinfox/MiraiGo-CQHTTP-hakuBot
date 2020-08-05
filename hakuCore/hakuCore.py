# hakuCore
# hakubot 内核
# 接受、处理并分发 go-cqhttp 传来的 json

from importlib import import_module
from hakuCore.botApi import *

def haku (msgList):
    if (msgList['raw_message'][0] == ':'):
        req = list(msgList['raw_message'].split(' ', 1))
        try:
            plgs = import_module('plugins.'+req[0][1:])
        except:
            pass
        else:
            print()
            plgs.main(msgList)
            return
