# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from hakuCore.botApi import *

def main (msgDict):
    helpMsg = '''小白现在懂得这些命令了哦:
[命令] help 获取帮助～
*开头的是管理员指令!
about
bc [args]
echo [args]
help
music [args]
log [args]
ping
time [args]
*atall [args]
*timertest [args]'''
    if msgDict['message_type'] == 'private':
        send_private_message(msgDict['user_id'], helpMsg)
    elif msgDict['message_type'] == 'group':
        send_group_message(msgDict['group_id'], helpMsg)
 
