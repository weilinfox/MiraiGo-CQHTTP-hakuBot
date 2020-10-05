# 此源代码的使用受 GNU AFFERO GENERAL PUBLIC LICENSE version 3 许可证的约束, 您可以在下面的链接找到该许可证.
# https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot/blob/master/LICENSE

from hakuCore.hakuCore import VERSION

def main (msgDict):
    aboutMsg = '小白哥哥是狸开发的qq机器人~\n'
    aboutMsg += '小白是小白哥哥 ' + VERSION + ' 的分身!\n'
    aboutMsg += '欢迎大佬贡献代码: https://github.com/weilinfox/MiraiGo-CQHTTP-hakuBot'
    return aboutMsg
