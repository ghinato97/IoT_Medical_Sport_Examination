from Sensori_Aggiornamento_Catalogo import *
from Accelerometro_Sensore_Prova import *
from Pulsossimetro import *
from Start_Stop import *
from Temperatura import *
from MyMQTT_TS import *
from MyMQTT import *

import time
import json
import requests


class Sensors_Run:
    def __init__(self,time):
        conf=json.load(open("Catalog.json",'r'))
        broker=conf["broker"]['IpAddress']
        broker_TS=conf["broker"]['IpAddress_TS']
        port=conf["broker"]['port']        
        channelID=conf['thingSpeak']['channelID']

        
        username=conf['thingSpeak']["username"]
        password=conf['thingSpeak']["password"]
        z=conf['thingSpeak']["channelID"]
        clientID=username
        
        self.update=Sensors_Update()

        self.topic='channels/'+str(channelID)+'/publish'
        self.topic_=conf["broker"]['topic']
        self.topic_but=self.topic_+'Emergency'
        self.client=MyMQTT(clientID,broker_TS,port,username,password,None)
        self.client_=MyMQTT_('Accelerometer',broker,port,self)
        self.time=time
        
        


        
            
    def start (self):
        self.client.start()
        self.client_.start()

    def stop (self):
        x=Start_Stop(0)
        message=json.loads(x.Start())        
        self.client_.myPublish(self.topic_+'Controller',message)     
        

        self.client.stop()
        self.client_.stop()
        
        
    def publish(self):
        self.update.Postare_Catalog()
                        
        time_start=int(time.time())
        self.start()
        x=Start_Stop(1)
        message=json.loads(x.Start())
        self.client_.myPublish(self.topic_+'Controller',message)
        time_refresh=time.time()
        while (time.time()-time_start)<=self.time:
            time.sleep(0.5)
            x=Accelerometro(random.randint(10,40))
            message=json.loads(x.Misura())        
            val=message['e'][0]['v']
            self.client_.myPublish(self.topic_+'Accelerometer', message)
            self.client_.myPublish(self.topic_+'Controller', message)
            
            
            sensor=Pulsossimetro()        
            message=json.loads(sensor.battito())
            val1=message['e'][0]['v'] 
            self.client_.myPublish(self.topic_+'Heart_Rate', message)
            
            message=json.loads(sensor.perfusione())
            val2=message['e'][0]['v'] 
            self.client_.myPublish(self.topic_+'Perfusion', message)
            message=json.loads(sensor.saturazione())
            val3=message['e'][0]['v']
            self.client_.myPublish(self.topic_+'Saturation', message)
            
            
            temp=Temperature()
            message=json.loads(temp.Misura())
            val4=message['e'][0]['v']
            self.client_.myPublish(self.topic_+'Temperature', message)
            
            
            
            tPayload='field1={}&field2={}&field3={}&field4={}&field5={}'.format(val,val1,val2,val3,val4)
            self.client.myPublish(self.topic,tPayload)
            if time.time()-time_refresh>60:
                self.update.Refresh()
                time_refresh=time.time()

            
        self.stop()
        

if __name__=='__main__':
    x=Sensors_Run(30)  
    x.publish()

        
