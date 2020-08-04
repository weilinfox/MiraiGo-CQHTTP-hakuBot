# MiraiGo-hakuBot

haku-bot，利用go-cqhttp快速构建的QQ机器人

## 依赖于

+ [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 使用 mirai 以及 MiraiGo 开发的cqhttp golang原生实现
+ Python3.x 开发时尽量使用较底层的标准库，在龙梦Fedora28平台开发测试，其他平台未知。

## 目的

用于Python的学习和交流。

## 快速上手

在 ``config.py`` 中设置监听的地址和端口等即可。

## 实现的功能

在终端打印收到的 raw_message

## 参考资料

+ [MiraiGo协议支持列表](https://github.com/Mrs4s/MiraiGo/blob/master/README.md)
+ [coolq-http-api](https://richardchien.gitee.io/coolq-http-api/docs/4.15/#/API)
+ [go-cqhttp扩展api](https://github.com/Mrs4s/go-cqhttp/blob/master/docs/cqhttp.md)

## 其他

go-cqhttp 需要交叉编译为 mips64le 。暂时没有官方的 mips64le release。



By SDUST weilinfox