# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

def main (msgDict):
    req = list(msgDict['raw_message'].split(' ', 1))
    if len(req) > 1:
        req[1] = req[1].strip()
        if len(req[1]) == 0: return
    else:
        return

    return req[1]
 
