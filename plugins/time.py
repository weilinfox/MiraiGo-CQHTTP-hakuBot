# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import time

def main (msgDict):
    helpMsg = '''小白还是知道北京时间的～
或者告诉小白你想要的时区(-12~+12)'''
    req = list(msgDict['raw_message'].split(' ', 1))
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

    if (len(req) > 1 and req[1].strip() == 'help'):
        return helpMsg
    else:
        return ans

#if __name__ == '__main__':
#    main({'message_type':'private', 'user_id':-1, 'raw_message':':time'})
