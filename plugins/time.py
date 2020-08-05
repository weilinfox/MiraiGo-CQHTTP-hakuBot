import time
from hakuCore.botApi import *

def main (msgList):
    helpMsg = '''小白还是知道北京时间的～
或者告诉小白你想要的时区(-12~+12)'''
    req = list(msgList['raw_message'].split(' ', 1))
    zone = 8
    ans = 'null'
    if len(req) > 1:
        try:
            zone = int(req[1])
        except:
            pass
    if zone < -12 or zone > 12:
        ans = '好像没有这个时区？'
    else:
        ans = time.asctime(time.gmtime(time.time() + zone * 3600))
        if zone > 0:
            ans += '\nUTC+' + str(zone)
        elif zone < 0:
            ans += '\nUTC' + str(zone)
        else:
            ans += '\nUTC'

    if msgList['message_type'] == 'private':
        if (len(req) > 1 and req[1].strip() == 'help'):
            send_private_message(msgList['user_id'], helpMsg)
        else:
            send_private_message(msgList['user_id'], ans)
    elif msgList['message_type'] == 'group':
        if (len(req) > 1 and req[1].strip() == 'help'):
            send_group_message(msgList['group_id'], helpMsg)
        else:
            send_group_message(msgList['group_id'], ans)

if __name__ == '__main__':
    main({'message_type':'private', 'user_id':2521857263, 'raw_message':':time'})
