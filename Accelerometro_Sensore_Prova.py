import json
import time
class Accelerometro(object):
    def __init__(self,acceleration):
       self.accelerazione=acceleration
       self.chiavi=['bn','e']
       self.chiavi1=['n','u','t','v']
         
    def Misura(self):
        k=[]
        valori1=['Acceleration','RPM',str(time.time()),self.accelerazione]
        diz=dict(zip(self.chiavi1,valori1))
        k.append(diz)
        valori=['IoT/sensors/accelerometer',k]
        SenML=dict(zip(self.chiavi,valori))
        SenML_json=json.dumps(SenML)
        return SenML_json
    
    
if __name__=="__main__":
    x=Accelerometro(3)
    c=x.Misura()
    

