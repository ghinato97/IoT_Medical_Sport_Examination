from Sensori_Aggiornamento_Catalogo import *
from Pulsossimetro import *
from Start_Stop import *
from MyMQTT import *

from threading import Thread
from pprint import pprint
import time
import json
import requests

def Start_Stop(x):
    chiavi = ['bn','e']
    chiavi1 = ['n','u','t','v']
    valore=x
    k = []
    valori1 = ['Status','On/Off',str(time.time()),valore]
    diz = dict (zip(chiavi1,valori1))
    k.append(diz)
    valori = ['IOT/sensore/EmergencyButton',k]
    SenML = dict(zip(chiavi,valori))
    SenML_json =json.dumps(SenML)
    return SenML_json

def Accelerometro():
   
   chiavi=['bn','e']
   chiavi1=['n','u','t','v']
   k=[]
   accelerazione=random.randint(10,40)
   valori1=['Acceleration','RPM',str(time.time()),accelerazione]
   diz=dict(zip(chiavi1,valori1))
   k.append(diz)
   valori=['IoT/sensors/accelerometer',k]
   SenML=dict(zip(chiavi,valori))
   SenML_json=json.dumps(SenML)
   return SenML_json
    

def Temperature():
   chiavi=['bn','e']
   chiavi1=['n','u','t','v']
   temp=random.randint(20,40)
   k=[]
   valori1=['Temperature','°C',str(time.time()),temp]
   diz=dict(zip(chiavi1,valori1))
   k.append(diz)
   valori=['IoT/sensors/temperature',k]
   SenML=dict(zip(chiavi,valori))
   SenML_json=json.dumps(SenML)
   return SenML_json
     
    

class Sensors_Run:
    def __init__(self):
        f=open('Catalog.json','r')
        cat=json.load(f) 
        
        url_base=cat['Catalog_uri'] 
        
        url=url_base+'/retrieve/broker'        
        broker=requests.get(url).text
        
        url=url_base+'/retrieve/port'
        port=requests.get(url).text
        port=int(port)
        
      
        self.update=Sensors_Update()

        clientID='Sensor_Run_Mexa_Iot_project'

        url=url_base+'/retrieve/topic'
        self.topic_=requests.get(url).text
        
        
        self.topic_controllo='Go/IoT_project_Mexa'

        self.client_=MyMQTT_(clientID,broker,port,self)
        
        self.flag=0
        
        
        self.diz={}
        
        url=url_base+'/retrieve/channels'
        r=requests.get(url).text
        channels=json.loads(r)
        for cha in channels:
            self.diz[str(cha)]={'kit':0,
                                'tempo':0,
                                'flag':0,
                                'pub':0,
                                'thread':0
                                    }
        
        
        
        self.start()
        
    def start(self):
        self.client_.start()
        self.client_.mySubscribe(self.topic_controllo)
    
    def notify(self,topic,message):
        messaggio=json.loads(message)
        
        kit=int(messaggio['kit'])
        tempo=int(messaggio['time'])
        channel=int(messaggio['channel'])
        
        self.flag=1
        
        self.diz[str(channel)]={'kit':kit,
                                'tempo':tempo,
                                'flag':1,
                                'pub':0,
                                'thread':0
                            
                                }
        

        


   
    def run(self): 
        while True:
            if self.flag==1:
                for keys in self.diz:
                    if self.diz[keys]['flag']==1 and self.diz[keys]['pub']==0:
                        self.diz[keys]['thread']=1                 
                        session_thread=Thread(target=self.pub).start()
                        self.diz[keys]['thread']=0
                        self.diz[keys]['flag']=0
                        time.sleep(1)
    
   
    def pub(self):
        for keys in self.diz:
            if  self.diz[keys]['thread']==1:
                print('entrato nel thread')
                
                self.diz[keys]['thread']=0
                
                self.update.Postare_Catalog()
                
                channel=keys
                kit= self.diz[keys]['kit']
                tempo=self.diz[keys]['tempo']
                
                sensor=Pulsossimetro()  
                
                topic_Accelerometro=self.topic_+'/'+str(channel)+'/'+str(kit)+'/Accelerometer'
                topic_Heart_Rate=self.topic_+'/'+str(channel)+'/'+str(kit)+'/Heart_Rate'
                topic_Perfusion=self.topic_+'/'+str(channel)+'/'+str(kit)+'/Perfusion'
                topic_Saturation=self.topic_+'/'+str(channel)+'/'+str(kit)+'/Saturation'
                topic_Temperature=self.topic_+'/'+str(channel)+'/'+str(kit)+'/Temperature'
                topic_Controller=self.topic_+'/'+str(channel)+'/'+str(kit)+'/Controller'
                
                x=Start_Stop(1)
                message=json.loads(x)        
                self.client_.myPublish(topic_Controller,message)   
                    
                
                time_start=time.time()
                time_refresh=time.time()
                
                while (time.time()-time_start)<=tempo:
                    time.sleep(0.5)
                    

                    message=json.loads(Accelerometro())
                    self.client_.myPublish(topic_Accelerometro, message)
                    
                    message=json.loads(Temperature())
                    self.client_.myPublish(topic_Temperature, message)
                    
                    message=json.loads(sensor.battito())   
                    self.client_.myPublish(topic_Heart_Rate, message)

                    
                    message=json.loads(sensor.perfusione())
                    val2=message['e'][0]['v'] 
                    self.client_.myPublish(topic_Perfusion, message)

                    
                    message=json.loads(sensor.saturazione())
                    self.client_.myPublish(topic_Saturation, message)
                    
            
                    
                    if time.time()-time_refresh>60:
                        self.update.Refresh()
                        time_refresh=time.time()
                        
                self.diz[keys]['flag']=0        
                x=Start_Stop(0)
                message=json.loads(x)        
                self.client_.myPublish(topic_Controller,message)
                
                
        
        
        
        
        
                    
                    
               

           
   
               
                    
                    



    

        
        


        
            

        

if __name__=='__main__':
    x=Sensors_Run()
    x.run()
    while True:
        pass
        
