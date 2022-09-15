from  MyMQTT import *
from Respiratory_Frequency import *
import json
import time

class Data_Temp:
    def __init__(self):
        conf=json.load(open("Catalog.json",'r'))
        broker=conf["broker"]['IpAddress']
        port=conf["broker"]['port']
        clientID='Data_Plot_Temp'
        
        self.temp_val=[]

        
        self.topic='IoT_Polito_Project/Sensor/Temperature'
        self.client=MyMQTT_(clientID,broker,port,self)
        self.time_start=int(time.time())
        
        
     
    def start (self):
        self.client.start()
        self.client.mySubscribe(self.topic)
        
    def stop (self):
        self.client.stop()
        
    def notify(self,topic,msg):        
        msg=json.loads(msg)
        valore=msg['e'][0]['v']
        now=int(time.time())
        if len(self.temp_val)<=10:
            self.temp_val.append(valore)
        else:
            BPM= Resp_Freq(self.temp_val).BPM()
            self.time_start=time.time()
            self.temp_val=[]
            topic='IoT_Polito_Project/Sensor/BPM'
            self.client.myPublish(topic,BPM)
            
            
                            
            
        
        
        
if __name__=='__main__':
    Data_Temp()
    Data_Temp().start()
    while True:
        x=0

          
