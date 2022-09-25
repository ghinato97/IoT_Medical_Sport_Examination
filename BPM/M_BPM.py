from  MyMQTT import *
from scipy.signal import find_peaks
import numpy as np
import pandas as pd
import json
import time
import requests

class Data_Temp:
    def __init__(self):
        conf=json.load(open("Catalog.json",'r'))
        url_base=conf['Catalog_uri']

        url=url_base+'/retrieve/broker'
        broker=requests.get(url).text
        
        url=url_base+'/retrieve/port'
        port=requests.get(url).text
        port=int(port)
       
        clientID='Data_Plot_Temp_Mexa_IoT_Project'
        

        url=url_base+'/retrieve/topic'
        self.topic=requests.get(url).text
        self.topic_generale=self.topic+'/#'
        
        
       
        self.client=MyMQTT_(clientID,broker,port,self)
        self.time_start=int(time.time())

        url2=url_base+'/retrieve/channels'
        r=requests.get(url2).text
        self.channelID=json.loads(r)
        
        self.diz={}
        for cha in self.channelID:
            self.diz.update({f'{cha}':[]})
        

     
    def start (self):
        self.client.start()
        self.client.mySubscribe(self.topic_generale)
        
    def stop (self):
        self.client.stop()
        
    def notify(self,topic,msg):        
        msg=json.loads(msg)
        x=topic.split("/")
        x.pop(3)
        topic='/'.join(x)
        
        for cha in self.channelID:
            self.topic_=self.topic+'/'+str(cha)+'/Temperature'
            if self.topic_==topic:
                valore=msg['e'][0]['v']
                x=self.diz[str(cha)]                               
                if len(x)<=10:
                    self.diz[str(cha)].append(valore)
                else:
                        self.diz[str(cha)]=[]
                        picchi=find_peaks(x)[0]
                        
                        time_diff=np.diff(picchi)
                        try:
                            time_diff=time_diff.mean()*0.5
                            #moltiplichiamo per 0.5 perchè i sensori pubblicano ogni 0.5 secondi
                            BPM= int(60/time_diff)
                            topic=self.topic+'/'+str(cha)+'/BPM'
                            self.client.myPublish(topic,BPM)
                        else:
                            pass
                        
            
            
                            
            
        
        
        
if __name__=='__main__':
    Data_Temp()
    Data_Temp().start()
    while True:
        x=0

          
