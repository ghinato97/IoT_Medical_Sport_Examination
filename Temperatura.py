import json
import time
import random

class Temperature():
    def __init__(self):
       self.chiavi=['bn','e']
       self.chiavi1=['n','u','t','v']
         
    def Misura(self):
        temp=random.randint(20,40)
        k=[]
        valori1=['Temperature','°C',str(time.time()),temp]
        diz=dict(zip(self.chiavi1,valori1))
        k.append(diz)
        valori=['IoT/sensors/temperature',k]
        SenML=dict(zip(self.chiavi,valori))
        SenML_json=json.dumps(SenML)
        return SenML_json
    
    
if __name__=="__main__":
    x=Temperature()
    c=x.Misura()
    

