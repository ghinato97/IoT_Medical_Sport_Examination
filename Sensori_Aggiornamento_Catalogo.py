
import threading
import time
import requests


class Sensors_Update:
    def __init__(self):
            threading.Timer(5.0,self.Postare_Catalog).start()

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
        url='http://127.0.0.1:8090/add/device'
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
        url='http://127.0.0.1:8090/add/device'
        r=requests.post(url,json=diz)
        print('\n Pulsossimetro: device registrato \n')
        
        
        threading.Timer(60.0,self.Refresh).start()
        
        
        
        
    def Refresh(self):
      url='http://127.0.0.1:8090/update/device'
      deviceName="Accelerometer"
      deviceId=1
      chiavi=["deviceName","deviceID"]
      val=[deviceName,deviceId]
      dizionario = dict(zip(chiavi,val)) 
      r=requests.put(url,json=dizionario)
      print('\n Accelerometro: device aggiornato\n')
      
      url='http://127.0.0.1:8090/update/device'
      deviceName="Pulsossimeter"
      deviceId=2
      chiavi=["deviceName","deviceID"]
      val=[deviceName,deviceId]
      dizionario = dict(zip(chiavi,val)) 
      r=requests.put(url,json=dizionario)
      print('\n Accelerometro: device aggiornato\n')
      
      threading.Timer(60.0,self.Refresh).start()
            