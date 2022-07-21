
import json
import time
import random

class EmergencyButton:
    
    
    def __init__(self):
    
        self.chiavi = ['bn','e']
        self.chiavi1 = ['n','u','t','v']
        
    def Button(self):
        k = []
        self.button =round(random.random())
        valori1 = ['Status','Status',str(time.time()),self.button]
        diz = dict (zip(self.chiavi1,valori1))
        k.append(diz)
        valori = ['IOT/sensore/EmergencyButton',k]
        SenML = dict(zip(self.chiavi,valori))
        SenML_json =json.dumps(SenML)
        return SenML_json
    
    
        
        