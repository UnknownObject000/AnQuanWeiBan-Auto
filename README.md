# 安全微伴自动学习程序

## 声明
1. 本项目基于 @FallenSigh 的 [WeibanTool](https://github.com/FallenSigh/WeibanTool) 项目进行修改适配
2. 此项目仅供学习交流，本人不对因使用此项目产生的任何后果负责
3. 此项目仅为GitHub镜像，项目原地址位于 [AnQuanWeiBan-Auto](http://git.unknownnetworkservice.com:8013/UnknownObject/AnQuanWeiBan-Auto)

## 实现原理
1. 使用API抓取课程列表（可得到每门课的课程ID）
2. 遍历每个课程，使用课程ID请求进入学习接口
3. 将课程ID上传给验证码接口，获取验证码图像
4. 将验证码图像显示在屏幕上，供用户点击
5. 将点击的坐标提交到验证码校验接口，获取methodToken
6. 使用methodToken请求课程完成接口，完成该课程学习
7. 重复步骤2-6，直至所有课程学习完成

## 使用方法

### 0. 安装所需库

本项目使用到的库（import语句）已列在下方：
```
import datetime
import json
import random
import requests
import time
import cv2
import os
import json
```

### 1. 需要抓取的内容

访问 [安全微伴网页版](https://weiban.mycourse.cn/) 并登录，使用浏览器的F12开发者工具抓取以下内容
 - X-Token：每次登录的ID，会随登录次数不同而改变，会超时自动过期。可寻找XXX.do请求进行抓取
 - user_id：用户ID，每个人唯一，不会改变
 - user_project_id：当前学习项目的ID，每次任务不同，可直接从地址栏中获得
 - tenant_code：学校ID，每个学校唯一

### 2. 将抓取到的内容填入main.py中

```
x_token = ''
user_id = ''
user_project_id = ''
tenant_code = ''
```

### 3. 运行main.py，当程序弹出验证码时进行验证。

程序提供5次自动验证码重试次数，超过5次会自动终止运行。该次数可在main.py中下面代码处修改
```
if (retry_cnt >= 5):
    print('验证码重试次数达到上限，系统自动退出')
    exit(-1)
```
