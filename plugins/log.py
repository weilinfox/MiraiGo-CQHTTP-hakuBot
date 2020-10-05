# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import time

recordMsg = []
heartbeats = []
threadSum = 0
threadTimeOut = 0
lock = False

def msgRate():
    global recordMsg
    return len(recordMsg)

def heartRate():
    global heartbeats
    return len(heartbeats)

def main (msgDict):
    global threadSum, threadTimeOut
    
    msgList = list(msgDict['raw_message'].split())
    if len(msgList) > 1 and msgList[1].strip() == 'help':
        return '可以查看小白的状态哦~'

    global lock, recordMsg, heartbeats
    while lock:
        pass
    lock = True
    rmsg = '流量: ' + str(msgRate())+'/min\n心跳: ' + str(heartRate()*5) + '\n线程: ' + str(threadSum) + '\n异常: ' + str(threadTimeOut)
    lock = False
    return rmsg


def check():
    global lock, recordMsg
    while lock:
        pass
    lock = True
    ntime = time.time()
    while len(recordMsg) > 0:
        if ntime - min(recordMsg) >= 60:
            recordMsg.remove(min(recordMsg))
        else:
            break
    while len(heartbeats) > 0:
        if ntime - min(heartbeats) >= 60:
            heartbeats.remove(min(heartbeats))
        else:
            break
    lock = False

def insert():
    global lock, recordMsg
    ntime = time.time()
    while lock:
        pass
    lock = True
    recordMsg.append(ntime)
    lock = False

def heartBeats():
    global lock, heartbeats
    ntime = time.time()
    while lock:
        pass
    lock = True
    heartbeats.append(ntime)
    lock = False
    
def threadStatus(thr, timeout):
    global threadSum, threadTimeOut
    threadSum = thr
    threadTimeOut = timeout
