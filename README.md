# wxrobot
微信机器人(基于网页版微信API)
#  [![star this repo](http://github-svg-buttons.herokuapp.com/star.svg?user=bobolau&repo=wxrobot&style=flat&background=1081C1)](http://github.com/bobolau/wxrobot) [![fork this repo](http://github-svg-buttons.herokuapp.com/fork.svg?user=bobolau&repo=wxrobot&style=flat&background=1081C1)](http://github.com/bobolau/wxrobot/fork) ![python](https://img.shields.io/badge/python-3.6-ff69b4.svg)

## 1. 微信机器人功能
主要特性：
#多微信帐号同时登录
#微信重启免登录（验证中）
#群助手（欢迎新人）
#群直播（主群消息转发到分发群)（完成部分工作）
#小号助手（主号代管小号） （开发中）
#个人自助聊天
#群自助聊天
#集成外部机器人
#docker容器
#插件机制（计划中）

## 2. 微信机器人部署
推荐基于docker部署
a. docker file
wxrobot/Dockerfile:
b. docker-compose
docker-compose.yml
wxrobot:
   restart: always
   build: ./wxrobot/

docker-compose build
docker-compose up -d

## 3. 参考信息
## Web Weixin Pipeline
## Web Weixin API
请参见Urinx/WexinBot的文档
```
       +--------------+     +---------------+   +---------------+
       |              |     |               |   |               |
       |   Get UUID   |     |  Get Contact  |   | Status Notify |
       |              |     |               |   |               |
       +-------+------+     +-------^-------+   +-------^-------+
               |                    |                   |
               |                    +-------+  +--------+
               |                            |  |
       +-------v------+               +-----+--+------+      +--------------+
       |              |               |               |      |              |
       |  Get QRCode  |               |  Weixin Init  +------>  Sync Check  <----+
       |              |               |               |      |              |    |
       +-------+------+               +-------^-------+      +-------+------+    |
               |                              |                      |           |
               |                              |                      +-----------+
               |                              |                      |
       +-------v------+               +-------+--------+     +-------v-------+
       |              | Confirm Login |                |     |               |
+------>    Login     +---------------> New Login Page |     |  Weixin Sync  |
|      |              |               |                |     |               |
|      +------+-------+               +----------------+     +---------------+
|             |
|QRCode Scaned|
+-------------+
```



