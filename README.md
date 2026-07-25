# 小智AI机器人：云端自动编译BIN

这个仓库不要求你的电脑安装ESP-IDF。

GitHub会在云端使用：

- 小智官方源码 v2.4.0
- ESP-IDF v6.0.2
- 自定义机器人板卡代码

自动编译并生成可下载的固件文件。

## 最简单的操作

1. 登录GitHub。
2. 创建一个新的空仓库。
3. 把本压缩包中的所有内容上传到仓库根目录。
4. 打开仓库顶部的 Actions。
5. 点击“编译小智机器人固件”。
6. 点击“Run workflow”。
7. 等待编译完成。
8. 在运行页面底部下载：
   `xiaozhi-robot-s3-firmware`
9. 解压后优先寻找：
   `merged-binary.bin`

## 烧录

使用乐鑫 Flash Download Tool：

- ChipType：ESP32-S3
- WorkMode：Develop
- LoadMode：UART
- 固件：merged-binary.bin
- 地址：0x0

先执行ERASE，再执行START。

## 第一次编译

自定义代码必须经过真实编译验证。

若Actions显示红色失败：
打开失败任务，把第一条真正的error开始到结束的日志复制给我。
我会按照实际小智v2.4.0接口修正代码。
