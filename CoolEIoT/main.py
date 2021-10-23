# -*- coding: utf-8 -*-  
import paho.mqtt.client as mqtt
import requests
import json
import time
import ssl
import traceback

APISERVER = "https://api.cooleiot.tech/"
MQTTSERVER = "broker.cooleiot.tech"
MQTTPORT = 1883
MQTTPORTSSL = 8883

class CoolE(object):
    def __init__(self, developkey):
        self.client_id = "coole-device-"
        self.topic = "cooleiot/"
        self.developkey = developkey
        self.headers = {
            "Content-Type": "application/json"
        }
        self.client = mqtt.Client(self.client_id)
        self.device_id = None
        self.is_debug = False
        self.recv = ""
        self.report_content = {}
        self.field_num = 0
        self.content_content = {}
        self.last_publish_time = 0
    
    def start(self, keepalive:int = 60, ssl:bool = False):
        global APISERVER,MQTTSERVER,MQTTPORT,MQTTPORTSSL
        url = APISERVER + "device/develop/" + self.developkey
        req_info = requests.get(url, headers=self.headers)
        info = json.loads(req_info.text)
        if info['code'] == 1000:
            self.client_id += info['data']['device_id'] + str(int(time.time()))
            self.topic += info['data']['username'] + "/" + info['data']['device_id']
            self.device_id = info['data']['device_id']
        else:
            self.debug(info)
            return
        self.client = mqtt.Client(self.client_id)
        self.client.username_pw_set(self.developkey)
        if ssl:
            self.client.tls_set()
            self.client.connect(MQTTSERVER, MQTTPORTSSL, keepalive)
        else:
            self.client.connect(MQTTSERVER, MQTTPORT, keepalive)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def loop(self):
        # self.client.loop_forever()
        self.client.loop_start()
    
    def stop(self):
        self.client.disconnect()
        time.sleep(0.1)

    def publish(self, field:str = None, payload = None):
        if time.time() - self.last_publish_time < 1 and self.last_publish_time != 0:
            time.sleep(time.time() - self.last_publish_time)
        if field is None and payload is None:
            # 发布所有updae过的字段消息
            publish_data = {
                'report': self.report_content
            }
            self.client.publish(self.topic, json.dumps(publish_data))
            self.last_publish_time = time.time()
        elif field is not None and payload is None:
            # 发布指定update过的字段消息 
            if self.report_content.get(field) is None:
                self.debug("无["+field+"]字段，请先update或检查是否clear")
                return
            publish_data = {
                'report':{
                    field: self.report_content[field]
                }
            }
            self.client.publish(self.topic, json.dumps(publish_data))
            self.last_publish_time = time.time()
        elif field is not None and payload is not None:
            # 手动发布指定字段的消息内容
            publish_data = {
                'report':{
                    field: payload
                }
            }
            self.client.publish(self.topic, json.dumps(publish_data))
            self.last_publish_time = time.time()
        else:
            self.debug("函数参数错误")
    
    def selfPublish(self, key, value):
        if time.time() - self.last_publish_time < 1 and self.last_publish_time != 0:
            time.sleep(time.time() - self.last_publish_time)
        publish_data = {
            key: value
        }
        self.client.publish(self.topic, publish_data)
        self.last_publish_time = time.time()
    
    def decode(self, payload:str, type:str):
        if payload == "" or payload is None:
            return None
        try:
            doc = json.loads(payload)
            if type == "COMMAND":
                result = doc.get("command")
            elif type == "GET":
                result = doc.get("get")
            elif type == "CONTENT":
                result = doc.get("content")
            else:
                result = None
            if result is not None:
                self.recv = None
            return result
        except Exception as e:
            self.debug("反序列化JSON时失败："+str(e))
            traceback.print_exc()
            return None
    
    def updateReport(self, field:str, data):
        if self.field_num > 30:
            self.debug("最多存储30个字段！")
            return
        self.report_content[field] = data
        self.field_num += 1
    
    def updateContent(self, field:str, data):
        self.content_content[field] = data
    
    def getReport(self, field:str):
        if self.report_content.get(field) is None:
            return None
        else:
            return self.report_content[field]
    
    def clearReport(self):
        self.report_content = {}
    
    def getContent(self, field:str):
        if self.content_content.get(field) is None:
            return None
        else:
            return self.content_content[field]

    def getConfig(self, field:str):
        url = APISERVER + "device/develop/" + self.developkey + "/config/" + field
        req_config = requests.get(url,headers=self.headers)
        config = json.loads(req_config.text)
        if config['code'] == 1000:
            return config['data']['config_content']['data']
        else:
            self.debug(config)

    def clearContent(self):
        self.content_content = {}

    def setDebug(self, sta:bool = True):
        self.is_debug = sta

    def debug(self, content):
        if self.is_debug:
            print("*CoolE: " + str(content))

    def getDeviceId(self):
        return self.device_id
    
    def on_connect(self, client, userdata, flags, rc):
        self.debug("MQTT连接结果： " + mqtt.connack_string(rc))
        if int(rc) == 0:
            self.debug("MQTT连接成功")
        self.client.subscribe(self.topic)

    def on_disconnect(self, client, userdata, rc):
        self.debug("MQTT连接断开：" + mqtt.connack_string(rc))

    def on_message(self, client, userdata, msg):
        self.recv = msg.payload.decode("utf-8")
        self.debug(msg.topic+": "+str(msg.payload.decode("utf-8")))