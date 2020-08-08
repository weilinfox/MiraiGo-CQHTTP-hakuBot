# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from hakuCore.botApi import *
import hakuCore.logging

allowUser = [805469904, 806009825]

def main (msgDict):
    global allowUser

    if not allowUser.count(msgDict['user_id']):
        if msgDict['message_type'] == 'private':
            send_private_message(msgDict['user_id'], '小白不认得你~')
        elif msgDict['message_type'] == 'group':
            send_group_message(msgDict['group_id'], '小白不认得你~')
        return

    msgList = list(msgDict['raw_message'].split(' ', 1))
    if len(msgList) > 1 and msgList[1].strip() == 'help':
        if msgDict['message_type'] == 'private':
            send_private_message(msgDict['user_id'], '发送消息给所有加入的群~')
        elif msgDict['message_type'] == 'group':
            send_group_message(msgDict['group_id'], '发送消息给所有加入的群~')
        return

    postMsg = ''
    for pos in range(1, len(msgList)):
        if pos != 1:
            postMsg += ' '
        postMsg += msgList[pos]
    rawList = get_group_list()
    #print(rawList)
    hakuCore.logging.directPrintLog('\n群发共 ' + str(len(rawList)) + ' 个群...')
    for itm in rawList:
        send_group_message(itm['group_id'], postMsg)
    hakuCore.logging.directPrintLog('\n群发完成')
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], '完工~')
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], '完工~')


