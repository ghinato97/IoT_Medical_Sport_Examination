import json
import time
from gpiozero import LED,Button
from Emergency_Button import *
from MyMQTT import *






class Control:
    def __init__(self):
        
        self.Led_verde=LED(2)
        self.Led_verde.off()
        self.Led_rosso=LED(3)
        self.Led_rosso.off()
        self.Led_start=LED(27)
        self.Led_start.off()
        
        self.Bottone=Button(17)
        
        self.val_max=30
        self.val_min=20


        conf=json.load(open("Catalog.json",'r'))
        broker=conf["broker"]['IpAddress']
        port=conf["broker"]['port']
        
        clientID='Control_Accelerometer'
          
        self.topic='IoT_Polito_Project/Sensor/Controller'
        self.topic_pub='IoT_Polito_Project/Sensor/Emergency'
        self.client=MyMQTT_(clientID,broker,port,self)
        
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)
    
    def stop(self):
        self.client.stop()
    
    def notify(self,topic,msg):
        messaggio=json.loads(msg)
        valore=messaggio['e'][0]['v']
        nome=messaggio['e'][0]['n']
        
        if nome=='Status':
            if valore==1:        
                self.Led_start.on() 
            if valore==0:
                self.Led_start.off()
        if nome=='Acceleration':
            if valore>self.val_max:
                self.Led_rosso.on()
                time.sleep(1)
                self.Led_rosso.off()
                time.sleep(1)
                
            if valore< self.val_min:
                self.Led_verde.on()
                time.sleep(1)
                self.Led_verde.off()
                time.sleep(1)
                    
    def publish(self):                      
        x=EmergencyButton()
        message=json.loads(x.Button())
        self.client.myPublish(self.topic_pub,message)

    def Press(self):
        self.Bottone.when_pressed=self.publish
        

        
    
        
        
        
        
if __name__=='__main__':
    x=Control()
    x.start()
    while True:
        x.Press()

	

    
