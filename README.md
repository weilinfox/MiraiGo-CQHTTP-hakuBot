# MiraiGo-CQHTTP-hakuBot

haku-bot，利用go-cqhttp在龙芯和其他平台快速构建的QQ机器人

## 依赖于

+ [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 使用 mirai 以及 MiraiGo 开发的cqhttp golang原生实现
+ Python3.6 尽量使用了较底层的标准库，在龙梦Fedora28平台编写测试，其他平台兼容性未知。

## 使用到的库

+ importlib
+ json
+ math
+ socket
+ threading
+ time

## 目的

用于Python的学习和交流。

## 快速上手

### 配置

在 ``hakuCore/config.py`` 中设置监听的地址和端口等即可。不带星号“*”的可以忽略保留默认值

+ BUF_SIZE socket接收和发送一个包的大小
+ TESTQQID 测试程序时私发消息的qq号
+ HOST 和go-cqhttp通信的ip *
+ RECEIVEPORT go-cqhttp上报消息的端口 *
+ SENDPORT cq-cqhttp接受消息的端口 *
+ TIKEN cq-cqhttp的access_token *
+ INTERVAL 用于定时任务检测时间的间隔

### 运行

``python3 main.py`` 运行。

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

### 两个线程

``main.py`` 创建了两个线程分别运行 ``server.py`` 和 ``timer.py`` 。 ``server.py`` 监听 go-cqhttp 的上报并将接收到的 json 转换为 dict ； ``timer.py`` 则提取当前时间，当当前时间和设定时间相同时触发相应事件，创建相应的 dict 。这个 dict 会被发送给 ``hakuCore/hakuCore.py`` 处理回应或再将其发送给 plugins 包下的相应插件回应。

### hakuCore

hakuCore 包是机器人的核心内涵，其中 ``config.py`` 用于参数设置， ``hakuCore.py`` 对所有信息进行处理和分发， ``botApi.py`` 作为回应 go-cqhttp 的接口， ``tcpSend.py`` （通常不需要手动调用）向 go-cqhttp 发送包。

``hakuCore.py`` 接受一个 dict ，这个 dict 和 go-cqhttp 上报的 json 格式一致，主要包含：

+ "message_type" 事件类型。群消息："group"，私发消息："private"
+ "group_id" 群号，群消息和临时会话有此字段
+ "user_id" QQ号，私发消息和临时会话有此字段
+ "raw_message" 信息，收到的信息
+ "message" 同"raw_message"
+ "self_id" 机器人自己的qq号

### 插件开发

所有插件在 plugins 目录下，命令名即文件名，使用“:”+命令名调用。如 ``ping`` 命令，对应插件名为 ``ping.py`` ，当hakuBot收到 ``:ping`` 时自动调用这个插件。

插件必须包含一个 ``main()`` 方法，其具有一个参数，当调用时会传给 ``main()`` 一个 dict ，这个 dict 包含这个事件的所有信息，其格式上面已经阐述。 ``main()`` 方法不需要返回值，即使有返回值也会被忽略。

插件可以做任何事，包括自由调用 ``plugins`` 和 ``hakuCore`` 下的任何模块。常见的是调用 ``hakuCore.botApi`` 下的方法发送消息进行回应。

虽然hakuBot还没有实现多线程，但最好还是考虑下多线程下可能出现的bug。

具体可以参考已经编写好的插件。

## 实现的功能

1. 在终端打印接收到消息的整个dict
2. 在终端打印发送消息的整个GET请求
3. 部分api可以通过函数调用

已经函数实现的 api 见 hakuCore/botApi.py

## 参考资料

+ [MiraiGo协议支持列表](https://github.com/Mrs4s/MiraiGo/blob/master/README.md)
+ [coolq-http-api](https://richardchien.gitee.io/coolq-http-api/docs/4.15/#/API)
+ [go-cqhttp扩展api](https://github.com/Mrs4s/go-cqhttp/blob/master/docs/cqhttp.md)

## 其他

+ go-cqhttp 需要交叉编译为 mips64le 。暂时没有官方的 mips64le release。
+ 程序中只是使用 socket 模拟了 http 协议的通信，虽然写 HTTP/1.0 但实际并没有完全遵循任何标准。
+ 只有在 ``main.py`` 调用 ``server.py`` 和 ``timer.py`` 时创建了两个线程，所以整个程序实际是阻塞式的。


By SDUST weilinfox
