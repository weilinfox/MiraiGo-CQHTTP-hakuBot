import time
from hakuCore.botApi import *

recordMsg = []
lock = False

def msgRate():
    global recordMsg
    return len(recordMsg)

def main (msgDict):
    msgList = list(msgDict['raw_message'].split())
    if len(msgList) > 1 and msgList[1].strip() == 'help':
        helpMsg = '可以查看小白的当前流量哦~'
        if msgDict['message_type'] == 'private':
            send_private_message(msgDict['user_id'], helpMsg)
        elif msgDict['message_type'] == 'group':
            send_group_message(msgDict['group_id'], helpMsg)
        return

    global lock, recordMsg
    while lock:
        pass
    lock = True
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], str(msgRate())+'/min')
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], str(msgRate())+'/min')
    lock = False


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
    lock = False

def insert():
    global lock, recordMsg
    ntime = time.time()
    while lock:
        pass
    lock = True
    recordMsg.append(ntime)
    lock = False
