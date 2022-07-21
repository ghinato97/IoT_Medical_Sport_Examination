from Sensori_Aggiornamento_Catalogo import *
from Accelerometro_Sensore_Prova import *
from Pulsossimetro import *
from EmergencyButton import *
from MyMQTT_TS import *
from MyMQTT import *
import time
import json


class Sensors_Run:
    def __init__(self):
        conf=json.load(open("Catalog.json",'r'))
        broker=conf["broker"]['IpAddress']
        broker_TS=conf["broker"]['IpAddress_TS']
        port=conf["broker"]['port']
        
        username=conf['thingSpeak']["username"]
        password=conf['thingSpeak']["password"]
        z=conf['thingSpeak']["channelID"]
        clientID=username
        
        Sensors_Update()

        self.topic='channels/'+str(1789105)+'/publish'
        self.topic_='IoT_Polito_Project/Sensor/Accelerometer'
        self.topic_but='IoT_Polito_Project/Sensor/Emergency'
        self.client=MyMQTT(clientID,broker_TS,port,username,password,None)
        self.client_=MyMQTT_('Accelerometer',broker,port,None)
        
        


        
            
    def start (self):
        self.client.start()
        self.client_.start()

    def stop (self):
        self.client.stop()
        self.client_.stop()
        
        
    def publish(self):
                        
        time_start=time.time()
        self.start()
        
        while (time.time()-time_start)<=30:
            time.sleep(1)
            x=Accelerometro(random.randint(10,40))
            message=json.loads(x.Misura())        
            val=message['e'][0]['v']
            self.client_.myPublish(self.topic_, message)
            
            x=EmergencyButton()
            message=json.loads(x.Button())
            self.client_.myPublish(self.topic_but, message)
            
            
            
            sensor=Pulsossimetro()        
            message=json.loads(sensor.battito())
            val1=message['e'][0]['v']        
            message=json.loads(sensor.perfusione())
            val2=message['e'][0]['v']        
            message=json.loads(sensor.saturazione())
            val3=message['e'][0]['v']
            tPayload='field1={}&field2={}&field3={}&field4={}'.format(val,val1,val2,val3)
            self.client.myPublish(self.topic,tPayload)
            print('published')
            
            
        self.stop()

        print('valore pubblicato')
        
if __name__=='__main__':
    x=Sensors_Run()
    time.sleep(3)
    x.publish()

        
