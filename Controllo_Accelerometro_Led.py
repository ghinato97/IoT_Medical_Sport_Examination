import json
import time
# from gpiozero import LED
from MyMQTT import *

# Led_verde=LED(2)
# Led_rosso=LED(3)

class Control_Accelerometer:
    def __init__(self):
        conf=json.load(open("Catalog.json",'r'))
        broker=conf["broker"]['IpAddress']
        port=conf["broker"]['port']
        
        # username=conf['thingSpeak']["username"]
        # password=conf['thingSpeak']["password"]
        # z=conf['thingSpeak']["channelID"]
        clientID='Control_Accelerometer'
          
        self.topic='IoT_Polito_Project/Sensor/Accelerometer'
        self.client=MyMQTT_(clientID,broker,port,self)
        
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)
    
    def stop(self):
        self.client.stop()
    
    def notify(self,topic,msg):
        val_max=30
        val_min=25
        messaggio=json.loads(msg)
        valore=messaggio['e'][0]['v']
        if valore>val_max:
            print('accendo led verd')
            Led_verde.pulse
        if valore< val_min:
            print('accendo led 2')
            Led_rosso.pulse
        

        
    
        
        
        
        
if __name__=='__main__':
    x=Control_Accelerometer()
    x.start()
    while True:
        time.sleep(1)
    x.stop()
    