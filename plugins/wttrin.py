# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

import hakuCore.logging
import requests

def main (msgDict):
    helpMsg = '狸的一个访问wttr.in的小玩意'
    req = list(msgDict['raw_message'].split())
    for i in range(0, len(req)):
        req[i] = req[i].strip()
    if i < 2:
        ans = helpMsg
    else:
        ans = '[CQ:image,file=http://wttr.in/' + req[1] + '_tqp0_lang=en.png]'

    return ans
 
