import time
import requests
import json

from  MyMQTT import *

class Timer():
    def __init__(self):
        f=open('Catalog.json','r')
        cat=json.load(f)   
        Catalog_uri=cat["Catalog_uri"]
        url=Catalog_uri+'/retrieve/url_bot'
        
        self.url_bot=requests.get(url).text

        
        url=Catalog_uri+'/retrieve/broker'
        self.broker=requests.get(url).text

        url=Catalog_uri+'/retrieve/port'
        self.port=requests.get(url).text
        self.port=int(self.port)
        
        self.client= MyMQTT_("timer_mexa_iot_project", self.broker, self.port,self)
        
        self.diz=[]
        
        

          
    def start(self):
        self.client.start()
        self.client.mySubscribe('timer/mexa')
        
    def stop(self):
        self.client.stop()

        
    def notify(self,topic,message):
        messaggio=json.loads(message)

        tempo=int(messaggio['tempo'])
        chat_id=int(messaggio['chat_id'])
        
        self.diz.append(chat_id)
        for i in range(len(self.diz)):
            if self.diz[i]==chat_id:
                time_start=time.time()
                while (time.time()-time_start)<=tempo:
                    pass
                url=self.url_bot+'/Session_End/'+str(self.diz[i])
                print(url)
                r=requests.get(url)
                
            self.diz.pop(0)



if __name__=='__main__':
    x=Timer()
    x.start()
    while True:
        pass
      
    
        

