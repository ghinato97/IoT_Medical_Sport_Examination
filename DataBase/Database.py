from MyMQTT import *
from MyMQTT_TS import *
import time
import pandas as pd
import numpy as np
import requests

class SendTS():
    def __init__(self):
        f=open('Catalog.json','r')
        self.cat=json.load(f) 
        
        url_base=self.cat['Catalog_uri'] 
        
        url=url_base+'/retrieve/broker'
        broker=requests.get(url).text
        
        url=url_base+'/retrieve/information_TS'
        broker_TS=requests.get(url).text
             
        url3=url_base+'/retrieve/username_TS'
        username=requests.get(url3).text
        
        url3=url_base+'/retrieve/password_TS'
        password=requests.get(url3).text
        
        clientID=username
        print(clientID)
        
        
        
        url=url_base+'/retrieve/port'
        port=requests.get(url).text
        port=int(port)
        
        
        
        url1=url_base+'/retrieve/topic'
        self.topic=requests.get(url1).text
        self.topic_generale=self.topic+'/#'

        url2=url_base+'/retrieve/channels'
        r=requests.get(url2).text
        self.channelID=json.loads(r)
        diz={}
        for cha in self.channelID:
            diz.update({f'{cha}':[0,0,0,0,0]})
        self.data_frame=pd.DataFrame.from_dict(diz)
            
    
        
        self.client=MyMQTT_(clientID,broker,port,self)
        self.client_TS=MyMQTT(clientID, broker_TS, port,username,password,notifier=None)
    
    def start(self):
        self.client.start()
        self.client_TS.start()
        
        self.client.mySubscribe(self.topic_generale)
       
    def stop(self):
        self.client.stop()
        self.client_TS.stop()
        
    def notify(self,topic,msg):
        messaggio=json.loads(msg)
        
        x=topic.split("/")
        # rimuovo la parte relativa al kit
        x.pop(3)
        #ricreo il topic senza il numero del lit
        topic='/'.join(x)

        
        for cha in self.channelID:
            self.topicA=self.topic+'/'+str(cha)+'/Accelerometer'
            self.topicH=self.topic+'/'+str(cha)+'/Heart_Rate'
            self.topicP=self.topic+'/'+str(cha)+'/Perfusion'
            self.topicS=self.topic+'/'+str(cha)+'/Saturation'
            self.topicT=self.topic+'/'+str(cha)+'/Temperature'
            
            
            if topic==self.topicA:
                self.data_frame[str(cha)][0]=int(messaggio['e'][0]['v'])
            if topic==self.topicH:
                self.data_frame[str(cha)][1]=int(messaggio['e'][0]['v'])
            if topic==self.topicP:
                self.data_frame[str(cha)][2]=int(messaggio['e'][0]['v'])
            if topic==self.topicS:
                self.data_frame[str(cha)][3]=int(messaggio['e'][0]['v'])
            if topic==self.topicT:
                self.data_frame[str(cha)][4]=int(messaggio['e'][0]['v'])
               
        for cha in self.channelID:
            x=self.data_frame[str(cha)].to_numpy()

            n_zero=np.count_nonzero(x)
            
            if n_zero==5:
                val1= self.data_frame[str(cha)][0]
                val2 = self.data_frame[str(cha)][1]
                val3= self.data_frame[str(cha)][2]
                val4= self.data_frame[str(cha)][3]
                val5= self.data_frame[str(cha)][4]
                
                
                tPayload='field1={}&field2={}&field3={}&field4={}&field5={}'.format(val1,val2,val3,val4,val5)
                topic_pub='channels/'+ str(cha) +'/publish'     
                self.client_TS.myPublish(topic_pub,tPayload)
                self.data_frame[str(cha)]=[0,0,0,0,0]
                
                


            
if __name__=="__main__":
    x=SendTS()
    time.sleep(1)
    x.start()
    while True:
        pass