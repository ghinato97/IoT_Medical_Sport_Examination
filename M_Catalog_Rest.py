import cherrypy
import json
import time
import threading

class Catalogo():
    exposed=True    
    
    def __init__(self):        
        f=open('Catalog.json','r')
        self.cat=json.load(f)   
        self.broker=self.cat['broker']
        self.devicesList=self.cat['devicesList']  
        self.userList=self.cat['usersList']
        threading.Timer(60.0,self.controllo).start()
        f.close()


                      

    def controllo(self): #il controllo elimina tutti gli elementi che siano antecedenti o precedenti i due minuti
        print('\n inizio controllo \n')
        f=open('Catalog.json','r')
        self.cat=json.load(f)
        self.start_time=int(time.time())
        self.devicesList=self.cat['devicesList']
        
        flag=[]
        for i in range(len(self.devicesList)):
            tempo=int(self.devicesList[i]['timeStamp'])
            diff=self.start_time-tempo
            if diff>120:
                flag.append(i)
        if len(flag)!=0:
            for k in range(len(flag)):  
                val=flag[-1]
                self.cat['devicesList'].pop(val)
                flag.pop(-1)
                print('\n device rimosso \n')
            with open('Catalog.json','w') as output:
                json.dump(self.cat,output)
                print("\n file modificato \n")
        threading.Timer(60.0,self.controllo).start()
            
            
                
                
        
        
    def GET(self,*uri,**params):            
        if len(uri)!=0:
            if uri[0]=='retrieve' and uri[1]=='information':
               IP=self.broker['IpAddress']
               port=self.broker['port']
               valore='Ip='+str(IP)+' e la porta è'+str(port)            
               return valore
           
            elif uri[0]=='retrieve' and uri[1]=='allDevices':
                devices=self.cat['devicesList']
                return str(devices)
          
            elif uri[0]=='retrieve' and uri[1]=='DevicesID':
                deviceID=int(params['deviceID'])
                for i in range(len(self.devicesList)):
                    if self.devicesList[i]['deviceId']==deviceID:
                        return str(self.devicesList[i])
                else:
                    testo='nessuno device trovato'
                    return testo     
               
                        
            elif uri[0]=='retrieve' and uri[1]=='UserID':
                usersList=self.cat['usersList']
                user_name=params['user_name']
                user_surname=params['user_surname']
                for i in range(len(usersList)):
                    if usersList[i]['Name']==user_name and usersList[i]['Surname']==user_surname:
                        return str(usersList[i])
                else:
                        testo='nessuno User trovato'
                        return testo
            else:
                return('azione non valida')
        else:
              return str('nessun comando immesso')
          
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()    
    def POST(self, *uri, **params): 
        if uri[0]=='add' and uri[1]=='device':
            data=cherrypy.request.json
            deviceName=data['deviceName']
            ID=data['deviceID']
            available_res=data['available_resources']
            end_point=data['end_point']
            tempo=time.time()
            local_time=time.ctime(tempo)
            chiavi=["deviceName","deviceID","available_resources","end_point","insert_time",'timeStamp']
            val=[deviceName,ID,available_res,end_point,local_time,tempo]
            
            for i in range(len(self.devicesList)):
                if self.devicesList[i]['deviceName']== deviceName and self.devicesList[i]['deviceID']==ID:
                    tempo=time.time()
                    local_time=time.ctime(tempo)
                    self.cat['devicesList'][i]['insert_time']=local_time
                    self.cat['devicesList'][i]['timeStamp']=tempo
                    with open('Catalog.json','w') as output:
                        json.dump(self.cat,output)
                        print('Device already registred, time updated')
                    return 0
        
            
            
            dizionario = dict(zip(chiavi,val))
            self.cat['devicesList'].append(dizionario)
            with open('Catalog.json','w') as output:
                json.dump(self.cat,output)
                print('\n device aggiunto \n')
                
        if uri[0]=='add' and uri[1]=='user':
            data=cherrypy.request.json
            userName=data['userName']
            userSurname=data['userSurname']
            # userID=data['userID']
            password=data['password']
            chiavi=["Name","Surname","password",'patient_list']
            lista=[]
            val=[userName,userSurname,password,lista]
        
            dizionario = dict(zip(chiavi,val))
            self.cat['usersList'].append(dizionario)
            with open('Catalog.json','w') as output:
                json.dump(self.cat,output)
                print('\n user aggiunto \n')
                
        if uri[0]=='add' and uri[1]=='patient':
            f=open('Catalog.json','r')
            self.cat=json.load(f)   
            self.userList=self.cat['usersList']
            
            
            data=cherrypy.request.json
            userName=data['User_name']
            print(userName)
            userSurname=data['User_surname']
            print(userSurname)
            patientName=data['Patient_name']
            print(patientName)
            patientSurname=data['Patient_surname']
            print(patientSurname)
            
            
            for i in range(len(self.userList)):
                if self.userList[i]['Name']==userName and self.userList[i]['Surname']==userSurname:
                    k={'Name':patientName,'Surname':patientSurname}
                    self.cat['usersList'][i]['patient_list'].append(k)
                    with open('Catalog.json','w') as output:
                        json.dump(self.cat,output)
                        print('\n paziente aggiunto \n')
                    
                    

            
                
        
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out() 
    def PUT(self,*uri,**params):
        if uri[0]=='update' and uri[1]=='device':
            data=cherrypy.request.json
            deviceName=data['deviceName']
            ID=data['deviceID']
            for i in range(len(self.devicesList)):
                if self.devicesList[i]['deviceName']==deviceName and self.devicesList[i]['deviceID']==ID:
                    tempo=time.time()
                    local_time=time.ctime(tempo)
                    self.cat['devicesList'][i]['insert_time']=local_time
                    self.cat['devicesList'][i]['timeStamp']=tempo
                    with open('Catalog.json','w') as output:
                        json.dump(self.cat,output)
                        print('\n tempo aggiornato \n')
                    
                        
                        
                
              





    
if __name__=="__main__":
    conf = {
    		'/': {
    			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    			'tools.sessions.on': True
    		}
    	}
    cherrypy.tree.mount(Catalogo(), '/', conf) 
    cherrypy.config.update({'server.socket_port': 8090})
    cherrypy.engine.start()
    cherrypy.engine.block()


