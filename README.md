# 酷易物联Python3SDK

酷易物联，快速接入/开发/管理物联设备
[cooleiot.tech](cooleiot.tech)

## 实例

实例化IoT连接，须填入设备的DevelopKey

```python
from CoolEIoT import CoolE
iot = CoolE("{developkey}")
```

### iot.setDebug

```python
# 设置debug状态
def setDebug(self, sta:bool = True)
```

使用：

```python
iot.setDebug()
```

### iot.recv

iot.recv 是 CoolE类的一个成员变量，用于存储当前从MQTT服务器接收到的消息

> 每当使用`iot.decode()`解析成功字段后，`iot.recv`将会重置清零

使用：

```python
recv = iot.recv
```

### iot.getDeviceId

```python
# 获取设备ID
def getDeviceId(self)
```

使用：

> 在`iot.start()`之后才能调用此方法获取设备ID

```python
device_id = iot.getDeviceId()
```


## 连接

### iot.start

```python
# 配置设备初始化并连接到MQTT服务器
def start(self, keepalive:int = 60, ssl:bool = False, host = False)
"""
keepalive: 默认60秒
ssl: 开启mqtts
host: 是否上位机(为True后，连接到mqtt服务器后不会触发上线)
"""
```

使用：

```python
iot.start()
iot.start(120)
iot.start(120, True)
```

### iot.loop

```python
# MQTT接收循环
def loop(self)
```

> 循环接收MQTT消息，如需要在设备运行过程中接收消息，**请将该方法放入主函数的`while True:`中**

使用：

```python
iot.loop()
```

### iot.stop

```python
# 关闭MQTT连接
def stop(self)
```

使用：

```python
iot.stop()
```

## 字段

### iot.decode

```python
# 字段解析
def decode(self, payload:str, type:str)
type = ["COMMAND","GET","CONTENT"]  # 命令字段，GET指令，内容字段
```

> 该方法用于解析在程序运行过程中接收到的三类字段

使用示例：

```python
def handleGet():
    get = iot.decode(iot.recv,"GET")
    if get is not None:
        print("接收到[" + get + "]GET指令")

def handleCommand():
    command = iot.decode(iot.recv,"COMMAND")
    if command is not None:
        print("接收到[" + command + "]命令字段")

def handleContent():
    content = iot.decode(iot.recv,"CONTENT")
    if content is not None:
        print("接收到[" + content['n'] + "]内容字段，内容为：" + content['d'])
```

---

> 开发中，您需要先将字段数据更新至iot实例中的一个成员变量，然后再进行消息发布<br />
也就是说，更新数据和发布消息是两步！

### iot.updateReport

```python
# 为通信字段添加一个字段内容
def updateReport(self, field:str, data)
```

> 该方法用于将数据更新至指定通信字段，相同字段名，后更新的数据会覆盖之前的数据

使用：

```python
iot.updateReport("temp",23.6)
iot.updateReport("ledsta","开")
```

### iot.getReport

```python
# 获取通信字段内容
def getReport(self, field:str)
```

使用：

```python
ledsta = iot.getReport("ledsta")
```

### iot.clearReport

```python
# 清除当前成员变量存储的所有通信字段信息
def clearReport(self)
```

使用：

```python
iot.clearReport()
```

### iot.updateContent

```python
# 为通信字段添加一个字段内容
def updateContent(self, field:str, data)
```

> 该方法用于将数据更新至指定内容字段，相同字段名，后更新的数据会覆盖之前的数据

使用：

```python
content = iot.decode(iot.recv,"CONTENT")
    if content is not None:
        iot.updateContent(content['n'],content['d'])
```

### iot.getContent

```python
# 获取通信字段内容
def getContent(self, field:str)
```

使用：

```python
print(iot.getContent("line1"))
```

### iot.clearContent

```python
# 清除当前成员变量存储的所有内容字段信息
def clearContent(self)
```

使用：

```python
iot.clearContent()
```

## 发布

> 为了避免代码编写不规范等导致的Broker阻塞<br />
无论代码编写方法如何，publish方法**每秒只会发送一条消息**

### iot.publish

```python
# 发布消息
def publish(self, field:str = None, payload = None)
```

#### 发布消息到MQTT服务器

 - 如果您想发送之前使用`iot.updateReport()`存储的**所有**通信字段内容

```python
iot.publish()
```

 - 如果您想发送之前使用`iot.updateReport()`存储的**指定**通信字段内容

```python
iot.publish("temp")
```

 - 如果您想发送指定通信字段内容的自定义内容，而不在其前面进行`updateReport()`。<br />
也就是说您想单独发送此次消息，而不将这次发送的数据更新到通信字段成员变量中

```python
iot.publish("temp",23.8)
iot.publish("ledsta","开")
```

### iot.selfPublish

 - 如果您想发送自定义key-value键值对

```python
iot.selfPublish("hello", "world")      # {"hello":"world"}
iot.selfPublish("ram", 400)            # {"ram":400}
iot.selfPublish("ram", "400")          # {"ram":"400"}
```

## 云配置

> 为了节省服务器资源，云配置每个DevelopKey每天仅能调用200次

### iot.getConfig

```python
# 获取云配置
def getConfig(self, field:str)
```

使用：

```python
citycode = iot.getConfig("citycode")
```