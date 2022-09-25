import json
import threading
import time
import requests


class Sensors_Update:
    def __init__(self):
            conf=json.load(open("Catalog.json",'r'))
            self.url_base=conf['Catalog_uri']
            self.time_start=time.time()

    
    
    def Postare_Catalog(self):
        available_res=["acceleration"]
        end_point="mqtt"
        tempo=time.time()
        local_time=time.ctime(tempo)
        deviceName='Accelerometer'
        deviceID=1
        chiavi=["deviceName","deviceID","available_resources","end_point","insert_time",'timeStamp']
        val=[deviceName,deviceID,available_res,end_point,local_time,tempo]        
        dizionario = dict(zip(chiavi,val))        
        url=self.url_base+'/add/device'
        r=requests.post(url,json=dizionario)
        print('\n Accelerometro: device registrato \n')
        
        available_res=["battito","perfusione","saturazione"]
        end_point="MQTT"
        tempo=time.time()
        local_time=time.ctime(tempo)
        deviceName='Pulsossimeter'
        deviceID=2
        chiavi=["deviceName","deviceID","available_resources","end_point","insert_time","timestamp"]
        valori=[deviceName,deviceID,available_res,end_point,local_time,tempo]    
        diz=dict(zip(chiavi,valori))
        url=self.url_base+'/add/device'
        r=requests.post(url,json=diz)
        print('\n Pulsossimetro: device registrato \n')
        
        available_res=["Temperature"]
        end_point="MQTT"
        tempo=time.time()
        local_time=time.ctime(tempo)
        deviceName='Temperature'
        deviceID=3
        chiavi=["deviceName","deviceID","available_resources","end_point","insert_time","timestamp"]
        valori=[deviceName,deviceID,available_res,end_point,local_time,tempo]    
        diz=dict(zip(chiavi,valori))
        url=self.url_base+'/add/device'
        r=requests.post(url,json=diz)
        print('\n Temperature : device registrato \n')
        

        
        
        
        
    def Refresh(self):
      self.time_start=time.time()  
      url=self.url_base+'/update/device'
      deviceName="Accelerometer"
      deviceId=1
      chiavi=["deviceName","deviceID"]
      val=[deviceName,deviceId]
      dizionario = dict(zip(chiavi,val)) 
      r=requests.put(url,json=dizionario)
      print('\n Accelerometro: device aggiornato\n')
      
      url=self.url_base+'/update/device'
      deviceName="Pulsossimeter"
      deviceId=2
      chiavi=["deviceName","deviceID"]
      val=[deviceName,deviceId]
      dizionario = dict(zip(chiavi,val)) 
      r=requests.put(url,json=dizionario)
      print('\n Pulsossimetro: device aggiornato\n')
      
      url=self.url_base+'/update/device'
      deviceName="Temperature"
      deviceId=3
      chiavi=["deviceName","deviceID"]
      val=[deviceName,deviceId]
      dizionario = dict(zip(chiavi,val)) 
      r=requests.put(url,json=dizionario)
      print('\n Temperature: device aggiornato\n')
      
      threading.Timer(60.0,self.Refresh).start()

            
