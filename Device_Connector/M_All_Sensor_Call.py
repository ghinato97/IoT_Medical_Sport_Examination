import cherrypy
import json
import time
import threading
from MyMQTT import *
from All_sensor_MQTT_TS_PUB import *

class All_Sensor_Pub():
    exposed=True    
    
    def __init__(self):        
        f=open('Catalog.json','r')
        self.cat=json.load(f) 
        
        url_base=self.cat['Catalog_uri'] 
        
        url=url_base+'/retrieve/broker'        
        broker=requests.get(url).text
        
        url=url_base+'/retrieve/port'
        port=requests.get(url).text
        port=int(port)
        
        url=url_base+'/retrieve/topic'
        self.topic_=requests.get(url).text
        self.topic_pub=self.topic_+'/go'
        print(self.topic_pub)
        
        clientID='Sensor_Calling_Mexa_IoT_Project'
        
        self.client_=MyMQTT_('clientID',broker,port,self)
        self.start()
        

    def GET(self,*uri,**params):            
        if len(uri)!=0:
            if uri[0]=='pub':
                channel=int(uri[1])
                kit=int(uri[2])
                time=int(uri[3])
                message={'channel':channel,
                         'kit':kit,
                         'time':time}
                self.client_.myPublish('Go/IoT_project_Mexa',message)
                print('pubblicato')
                return ('Public MQTT')
            else:
                return 0
            
    def start (self):
        self.client_.start()

    def stop (self):
        self.client_.stop()
                
              





    
if __name__=="__main__":
    conf = {
    		'/': {
    			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    			'tools.sessions.on': True
    		}
    	}
    cherrypy.tree.mount(All_Sensor_Pub(), '/', conf) 
    cherrypy.config.update({'server.socket_port': 8091})
    cherrypy.engine.start()
    cherrypy.engine.block()


