from time import strftime, gmtime, time
from hakuCore.botApi import *

lastMsgDict = {}

def printLog(logType, logInfo):
    print('\n[', strftime("%a, %m %b %Y %H:%M:%S GMT", gmtime()),
           '](' + logType + '): ', logInfo)


def newMsgLog(msgDict):
    global lastMsgDict

    # 只留下群消息
    if not msgDict.get('raw_message'):
        return
    elif msgDict['message_type'] != 'group':
        return

    if not lastMsgDict.get(msgDict['group_id']):
        lastMsgDict.update({msgDict['group_id']:[msgDict['user_id'], msgDict['raw_message'], msgDict['time'], False]})
    else:
        if lastMsgDict[msgDict['group_id']][1] == msgDict['raw_message']:
            if not lastMsgDict[msgDict['group_id']][3] and msgDict['time'] - lastMsgDict[msgDict['group_id']][2] < 60 \
               and lastMsgDict[msgDict['group_id']][0] != msgDict['user_id']:
                send_group_message(msgDict['group_id'], msgDict['raw_message'])
                lastMsgDict[msgDict['group_id']][3] = True
            
            lastMsgDict[msgDict['group_id']][0] = msgDict['user_id']
            lastMsgDict[msgDict['group_id']][2] = msgDict['time']
                
        else:
            lastMsgDict[msgDict['group_id']] = [msgDict['user_id'], msgDict['raw_message'], msgDict['time'], False]
    
