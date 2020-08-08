# 返回一个 list
# retcode 为 0 同时 status 为 ok 则响应成功，返回数据在 data 字段
# retcode 为 -1 同时 status 为 tcpSendError 则函数发生未知错误
# 其他值则代表其他错误，具体见 coolq-http-api 的文档，发生错误时 data 字段无数据

from hakuCore.tcpSend import uploadMessage

# 发送私聊消息
def send_private_message (userId, message, auto_escape=False):
    return uploadMessage('send_private_msg', {'user_id':userId, 'message':message, 'auto_escape':auto_escape})

# 发送群消息
def send_group_message (groupId, message, auto_escape=False):
    return uploadMessage ('send_group_msg', {'group_id':groupId, 'message':message, 'auto_escape':auto_escape})

# 发送讨论组消息
def send_discuss_message (discussId, message, auto_escape=False):
    return uploadMessage ('send_discuss_msg', {'discuss_id':discussId, 'message':message, 'auto_escape':auto_escape})

# 获取好友列表
def get_friend_list():
    return uploadMessage ('get_friend_list', {})

# 获取群列表
def get_group_list():
    dataDict = uploadMessage ('get_group_list', {})
    return dataDict['data']

# 获取群成员列表
def get_group_member_list(groupId):
    return uploadMessage ('get_group_member_list', {'group_id':groupId})
