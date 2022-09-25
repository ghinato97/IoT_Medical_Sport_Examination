import json
import time
# from gpiozero import LED,Button
from Emergency_Button import *
from MyMQTT import *
import requests


class Control:
    def __init__(self,kit):
        
        self.Led_verde=LED(2)
        self.Led_verde.off()
        self.Led_rosso=LED(3)
        self.Led_rosso.off()
        self.Led_start=LED(27)
        self.Led_start.off()
        
        self.Bottone=Button(17)
        
        self.val_max=30
        self.val_min=20
        
        self.kit=kit


        conf=json.load(open("Catalog.json",'r'))

        url_base=conf['Catalog_uri']
        
        url=url_base+'/retrieve/broker'
        broker=requests.get(url).text
        
        url=url_base+'/retrieve/port'
        port=requests.get(url).text
        port=int(port)
        
        url=url_base+'/retrieve/url_control'
        self.url_control=requests.get(url).text
        
        clientID='Kit_1_projectIoT'
        
        url=url_base+'/retrieve/topic'        
        self.topic_base=requests.get(url).text
        
        self.topic=self.topic_base+'/#'
        
        self.topic_pub=self.topic_base+'/Emergency'
        self.client=MyMQTT_(clientID,broker,port,self)
        
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic)
    
    def stop(self):
        self.client.stop()
    
    def notify(self,topic,msg):
        messaggio=json.loads(msg)
        valore=messaggio['e'][0]['v']
        x=topic.split("/")
        kit=int(x[3])
        tipo=x[4]
        
        if kit==self.kit:
        
            if tipo=='Controller':
                if valore==1:     
                    self.Led_start.on() 
                    print('start')
                if valore==0:
                    self.Led_start.off()
                    print('stop')
            elif tipo=='Accelerometer':
                if valore>int(self.val_max):
                    self.Led_rosso.on()
                    time.sleep(1)
                    self.Led_rosso.off()
                    time.sleep(1)
                    print('up')
                    
                if valore<int(self.val_min):
                    self.Led_verde.on()
                    time.sleep(1)
                    self.Led_verde.off()
                    time.sleep(1)
                    print('down')
                
                    
    def publish(self):                      
        x=EmergencyButton()
        message=json.loads(x.Button())
        valore=message['e'][0]['v']
        requests.get(self.url_control+'/Emergency/'+str(self.kit)+'/'+str(valore))

    def Press(self):  
        self.Bottone.when_pressed=self.publish
        

        
    
        
        
        
        
if __name__=='__main__':
    x=Control(1)
    x.start()
    while True:
        x.Press()
        pass

	

    
