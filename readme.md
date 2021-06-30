## 使用floodlight加python配置控制器流表

### 环境

- **树莓派ZERO_WH(RPIOS_lite系统,基于debian)**

    _[安装mininet和floodlight,编写sh脚本自启运行,作服务器用]_

- **任意主机**
    
    _[需包含python2/3含必要的库]_

### 逻辑

    1.流进入openflow交换机
    2.交换机查看转发表如果有匹配值，该开关将根据转发表指令转发该数据包。匹配可以是粗糙的匹配，就像传统的ACL
    3.如果交换机中没有匹配流，则触发事件，创建到控制器的数据包，在那里可以处理以下代码中的逻辑
    4.在控制器确定了一个操作后，创建一个输出包，告诉交换机将对该流和该流中的后续包采取什么操作

### pi端(server)

- **安装环境**

```bash
sudo apt install build-essential python python-dev python3 openjdk-8-jdk ant git mininet
git clone git://github.com/floodlight/floodlight.git
cd floodlight
git checkout v0.90
ant

cd floodlight/target && java -jar floodlight.jar
#后台运行使用
cd floodlight/target && java -jar floodlight.jar > /dev/null &
#将编辑的mininet(.mn /.py)导入运行
sudo ./<filename>.py
#CLI中可使用pingall测试连通性
```

- **自启动程序**

```bash

```

### 任意主机(client)

- **Python程序**

```python

```

- **解析**

    aaabbb