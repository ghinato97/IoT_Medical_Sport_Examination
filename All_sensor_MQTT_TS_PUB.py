from Sensori_Aggiornamento_Catalogo import *
from Accelerometro_Sensore_Prova import *
from Pulsossimetro import *
from MyMQTT_TS import *
import time
import json


class Sensors_Run:
    def __init__(self):
        conf=json.load(open("Catalog.json",'r'))
        broker=conf["broker"]['IpAddress']
        port=conf["broker"]['port']
        
        username=conf['thingSpeak']["username"]
        password=conf['thingSpeak']["password"]
        z=conf['thingSpeak']["channelID"]
        clientID=username
        
        Sensors_Update()

        self.topic='channels/'+str(1789105)+'/publish'
        self.client=MyMQTT(clientID,broker,port,username,password,None)
        
        


        
            
    def start (self):
        self.client.start()

    def stop (self):
        self.client.stop()
        
        
    def publish(self):
                        
        time_start=time.time()
        self.start()
        
        while (time.time()-time_start)<=100:
            time.sleep(15)
            x=Accelerometro(random.randint(10,40))
            message=json.loads(x.Misura())        
            val=message['e'][0]['v']
            
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
    x.publish()

        
