import json
import time
import requests
import cherrypy

class Controllo_emergency:
    
    exposed=True
    def __init__(self):
        
        conf=json.load(open("Catalog.json",'r'))
        self.url_base=conf['Catalog_uri']
        

        url=self.url_base+'/retrieve/url_bot'
        self.url_bot=requests.get(url).text
    

    def GET(self,*uri,**params):            
        if len(uri)!=0:
            if uri[0]=='Emergency':
              kit=uri[1]
              valore=int(uri[2])
              if valore==1:
            
               url=self.url_bot+'/Emergency/'+kit
               r=requests.get(url)
    
                    
            
if __name__=="__main__":
    
    x=Controllo_emergency()
    conf = {
    		'/': {
    			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    			'tools.sessions.on': True
    		}
    	}
    cherrypy.tree.mount(x, '/', conf) 
    cherrypy.config.update({'server.socket_port': 8093})
    cherrypy.engine.start()
    cherrypy.engine.block()

