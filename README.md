# MiraiGo-CQHTTP-hakuBot

haku-bot，小白哥哥：具有灵活的插件机制，利用go-cqhttp在龙芯和其他平台快速构建的QQ机器人。

## 实现的功能

### 主程序

1. 程序启动时线程启动失败重试
2. 在终端打印接收到消息的整个dict
3. 在终端打印发送消息的整个GET请求
4. 在终端打印错误信息
5. 定时在终端打印机器人流量
6. 部分api可以通过函数调用
7. 智zhi能zhang复读机
8. 群提醒（支持命令）
9. 欢迎新人
10. 被at回复

已经函数实现的 api 见 hakuCore/botApi.py

### 插件

+ about 回复关于信息
+ help 回复帮助信息
+ ping 检测机器人是否在工作
+ echo 人类的本质
+ time 回复指定时区的当前时间
+ bc 简单的四则运算计算器
+ music 网易云音乐搜索
+ qqmusic qq音乐搜索
+ weather 和风天气实时
+ forecast 和风天气预报
+ yiyan 一言搜索
+ log 返回小白的状态
+ timertest* 自动提醒测试
+ atall* 群发消息

ps: 带*为管理员指令，可在插件中分别设置允许的QQ id

## 依赖于

+ [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 使用 mirai 以及 MiraiGo 开发的cqhttp golang原生实现
+ Python3.6 尽量使用了较底层的标准库，在龙梦Fedora28平台编写测试，**不考虑Windows平台兼容性**。

## 使用到的库

### 主程序

+ importlib
+ json
+ math
+ os
+ random
+ socket
+ threading
+ time

### 插件额外依赖

+ requests: qqmusic, yiyan, weather

## 目的

用于Python的学习和交流。

## 快速上手

### 配置

在 ``hakuCore/config.py`` 中设置监听的地址和端口等即可。带星号“*”的字段必须重新设置并保证其正确性，其他字段可以保留其默认值

+ BUF_SIZE socket接收和发送一个包的大小
+ TESTQQID 测试程序时私发消息的qq号
+ HOST 和go-cqhttp通信的ip *
+ RECEIVEPORT go-cqhttp上报消息的端口 *
+ SENDPORT cq-cqhttp接受消息的端口 *
+ TIKEN cq-cqhttp的access_token *
+ INTERVAL 每分钟go-cqhttp发送的心跳个数，默认12
+ PROFIX 命令前缀设置，默认 ``':'`` (不包含引号)

### 运行

``python3 main.py`` 运行，也可以通过脚本 ``./haku.sh`` 运行。

若在远程服务器上运行需要用 screen 等工具挂在后台。

### 停止运行

有两种方式可以停止程序的运行。

+ 终端 Ctrl+C（按一次即可，按多次可能造成结束工作被打断！）
+ 向程序接受go-cqhttp上报消息的端口（即HOST:RECEIVEPORT）发送一个POST请求。请求头中包含 ``X-Self-Id`` 关键字，值为 ``1009`` ；包含 ``Content-Length`` 关键字，值为 ``0`` 。

POST请求示例（可以参考 main.py 中的 sendQuitPackage() 函数）：

```
POST / HTTP/1.0
X-Self-Id: 1009
Connect-Length: 0


```

### server

``main.py`` 创建了一个线程运行 ``server.py`` 。 ``server.py`` 监听 go-cqhttp 的上报并将接收到的 json 转换为 dict ，并调用 ``hakuCore/hakuCore.py`` 。如果是心跳，则会调用 ``hakuTime()`` 触发时间时间；反之把 dict 发送给 ``haku()`` 函数处理回应或再将其发送给 plugins 包下的相应插件回应。

### hakuCore

hakuCore 包是机器人的核心内涵，其中 ``config.py`` 用于参数设置， ``hakuCore.py`` 对所有信息进行处理和分发， ``botApi.py`` 作为回应 go-cqhttp 的接口， ``tcpSend.py`` （通常不需要手动调用）向 go-cqhttp 发送包， ``logging.py`` 打印和记录日志以及自动复读机的实现， ``timeEvent.py`` 读取时间事件相关文件。

``hakuCore.py`` 接受一个 dict ，这个 dict 和 go-cqhttp 上报的 json 格式一致，主要包含：

+ "message_type" 事件类型。群消息："group"，私发消息："private"
+ "group_id" 群号，群消息和临时会话有此字段
+ "user_id" QQ号，私发消息和临时会话有此字段
+ "raw_message" 信息，收到的信息
+ "message" 同"raw_message"
+ "self_id" 机器人自己的qq号

``hakuCore.py`` 主要有两个方法： ``haku()`` 和 ``hakuTime()`` 。 ``haku()`` 负责消息触发的事件， ``server.py`` 收到消息后会传到这里处理； ``hakuTime()`` 则负责时间触发的事件， ``server.py`` 收到心跳后会触发 ``hakuTime()`` 一次，该事件由 ``hakuTime()`` 和 ``timeEvent.py`` 协同处理。

### timeEvent

``hakuCore/timeEvent.py`` 读取时间相关事件的配置，这些配置是在 ``data/groupDay`` 文件夹中的纯文本文件。**它们都以对应的群号或QQ号命名，且均没有后缀。**如群号123的配置文件，文件名即为 ``123`` ；同理QQ号为456的用户的配置文件，文件名即为 ``456`` 。这个功能通常用于定时提醒。

配置均遵循一行一个记录，时间戳+空格+消息文本。按日提醒则时间戳以 ``mmdd`` 格式，按时间提醒则时间戳以 ``hhmm`` 格式。如每年十月一日自动发送“祖国母亲生日快乐”： ``1001 祖国母亲生日快乐`` ；每天晚上十点自动发送“晚安”： ``2200 晚安`` 。消息文本内可以有空格但是不能有换行，并列的多余空格会被忽略而只有一个空格，格式错误的记录会被忽略或消息文本发送不全。

若记录以命令格式开头，则发送给对应的插件执行；若出错，则按原文本发送。

已经实现时间事件的有：

1. 群内按日提醒：配置放在 ``data/groupDay`` 文件夹中，在凌晨零点发送（可以在 hakuCore/hakuCore.py 中更改）。
2. 群内每日按时间提醒：配置放在 ``data/groupTime`` 文件夹中。


### logging

``hakuCore/logging.py`` 用于日志的记录，日志文件在 ``data/log`` 文件夹下，日志第一行是程序启动的时间，重启程序并不会覆盖日志，旧日志会被重命名。

``hakuCore/logging.py`` 中 ``printLog(logType, logInfo)`` 和 ``directPrintLog(logInfo)`` 两个函数在将日志信息打印在终端的同时在日志文件中记录之，所以推荐用 ``directPrintLog(logInfo)`` 代替 ``print()`` ，以防一些错误被遗漏。 ``printLog(logType, logInfo)``  则会在信息上加上时间戳， ``logType`` 是自定义的错误类型，如 "ERROR"、"INFO" 等。

### 插件开发

所有插件在 plugins 目录下，命令名即文件名，使用 ``PREFIX`` +命令名调用。 ``PREFIX`` 在 ``hakuCore/config.py`` 中设置，默认为 ``'：'`` 。如 ``ping`` 命令，对应插件名为 ``ping.py`` ，当hakuBot收到 ``:ping`` 时自动调用这个插件。

插件必须包含一个 ``main()`` 方法，其具有一个参数，当调用时会传给 ``main()`` 一个 dict ，这个 dict 包含这个事件的所有信息，其格式上面已经阐述。 ``main()`` 方法不需要返回值，即使有返回值也会被忽略。

插件可以做任何事，包括自由调用 ``plugins`` 和 ``hakuCore`` 下的任何模块。常见的是调用 ``hakuCore.botApi`` 下的方法发送消息进行回应。

虽然hakuBot还没有实现多线程，但最好还是考虑下多线程下可能出现的bug。

具体可以参考已经编写好的插件。

## 参考资料

+ [MiraiGo协议支持列表](https://github.com/Mrs4s/MiraiGo/blob/master/README.md)
+ [coolq-http-api](https://richardchien.gitee.io/coolq-http-api/docs/4.15/#/API)
+ [go-cqhttp扩展api](https://github.com/Mrs4s/go-cqhttp/blob/master/docs/cqhttp.md)

## 其他

+ go-cqhttp 需要交叉编译为 mips64le 。暂时没有官方的 mips64le release。
+ 程序中只是使用 socket 模拟了 http 协议的通信，虽然写 HTTP/1.0 但实际并没有完全遵循任何标准。
+ 不要直接用 print 在终端显示信息，而用 ``hakuCore.logging`` 中的 ``printLog`` 和 ``directPrintLog`` 代替 。
+ 不知道哪里的问题，程序退出以后端口并没有立即释放，重启间隔一分钟内会出现端口占用的错误。
+ [我的小文章](https://www.cnblogs.com/weilinfox/p/13466407.html)


By SDUST weilinfox

