import cherrypy
import json
import time
import threading
from All_sensor_MQTT_TS_PUB import *

class All_Sensor_Pub():
    exposed=True    
    
    def __init__(self):        
        f=open('Catalog.json','r')
        self.cat=json.load(f)   
        self.broker=self.cat['broker']
        self.devicesList=self.cat['devicesList']  
        self.userList=self.cat['usersList']
      
        f.close()
        
        
    def GET(self,*uri,**params):            
        if len(uri)!=0:
            if uri[0]=='pub':
                time=float(uri[1])
                x=Sensors_Run(time)
                x.start()
                x.publish()
                return ('Public MQTT')
            else:
                return 0
            
                
              





    
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


