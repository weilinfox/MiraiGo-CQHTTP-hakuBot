# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

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

    msgList = list(msgDict['raw_message'].split())
    if len(msgList) > 1 and msgList[1].strip() == 'help':
        if msgDict['message_type'] == 'private':
            send_private_message(msgDict['user_id'], '用来测试timer~')
        elif msgDict['message_type'] == 'group':
            send_group_message(msgDict['group_id'], '用来测试timer~')
        return

    # 重载配置
    hakuCore.timeEvent.load()

    tm = time.gmtime(time.time() + 8*3600)
    ansStr = '***' + time.strftime("%02m/%02d", tm) + '***'
    strDict = hakuCore.timeEvent.searchGroupDate(time.strftime("%02m%02d", tm))
    for key in strDict.keys():
        ansStr += '\n+ ' + str(key) + '\n' + strDict[key]
    tm = time.gmtime(time.time() + 32*3600)
    ansStr += '\n***' + time.strftime("%02m/%02d", tm) + '***'
    strDict = hakuCore.timeEvent.searchGroupDate(time.strftime("%02m%02d", tm))
    for key in strDict.keys():
        ansStr += '\n+ ' + str(key) + '\n' + strDict[key]
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], ansStr)
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], ansStr)
    return

