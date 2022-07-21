
from MyMQTT import *
from EmergencyButton import *
import time
import json
import requests
import threading

class Sensor:
    def __init__(self,broker,port): 
        self.topic='Group/IoT/Sensors/Emercency_Button'
        self.clientID='EmergencyButton'
        self.client=MyMQTT(self.clientID,broker,port,None)
        self.deviceName="EmergencyButton"
        self.deviceId=3
        threading.Timer(5.0,self.Postare).start()

    def Postare(self):
        available_res=["Status"]
        end_point="mqtt"
        tempo=time.time()
        local_time=time.ctime(tempo)
        chiavi=["deviceName","deviceID","available_resources","end_point","insert_time",'timeStamp']
        val=[self.deviceName,self.deviceId,available_res,end_point,local_time,tempo]        
        dizionario = dict(zip(chiavi,val))        
        url='http://127.0.0.1:8090/add/device'
        r=requests.post(url,json=dizionario)
        print('\n device registrato \n')
        threading.Timer(60.0,self.Refresh).start()
        
        
    def Refresh(self):
     url=url='http://127.0.0.1:8090/update/device'
     deviceName="EmergencyButton"
     deviceId=3
     chiavi=["deviceName","deviceID"]
     val=[self.deviceName,self.deviceId]
     dizionario = dict(zip(chiavi,val)) 
     r=requests.put(url,json=dizionario)
     print('\n device aggiornato\n')
     threading.Timer(60.0,self.Refresh).start()
            

    def start (self):
        self.client.start()

    def stop (self):
        self.client.stop()


    
    def publish(self):
        x=EmergencyButton()
        xx=x.Button()
        message=json.loads(xx)
        tempo=time.time()
        local_time = time.ctime(tempo)
        message['e'][0]['t']=str(local_time)
        self.client.myPublish(self.topic,message)
        print("published")
        print(str(message))

if __name__ == "__main__":
    conf=json.load(open("settings_mqtt.json"))
    broker=conf["broker"]
    port=conf["port"]

    
    
    Manager= Sensor(broker,port)
    Manager.client.start()
    
    
 
    while True:
        Manager.publish()
        time.sleep(1)
    

    Manager.client.stop()   
