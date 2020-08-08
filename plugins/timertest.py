from hakuCore.botApi import *
import hakuCore.timeEvent
import time

allowUser = [805469904, 806009825]

def main (msgDict):
    global allowUser

    if not allowUser.count(msgDict['user_id']):
        if msgDict['message_type'] == 'private':
            send_private_message(msgDict['user_id'], '小白不认得你~')
        elif msgDict['message_type'] == 'group':
            send_group_message(msgDict['group_id'], '小白不认得你~')
        return

    tm = time.gmtime(time.time() + 8*3600)
    ansStr = time.strftime("%02m/%02d", tm) + '\n'
    ansStr += str(hakuCore.timeEvent.searchGroupDate(time.strftime("%02m%02d", tm)))
    tm = time.gmtime(time.time() + 32*3600)
    ansStr += '\n' + time.strftime("%02m/%02d", tm) + '\n'
    ansStr += str(hakuCore.timeEvent.searchGroupDate(time.strftime("%02m%02d", tm)))
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], ansStr)
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], ansStr)
    return

