import numpy as np
import json
import time
import random

class Start_Stop:
    
    
    def __init__(self,x):
    
        self.chiavi = ['bn','e']
        self.chiavi1 = ['n','u','t','v']
        self.valore=x
        
    def Start(self):
        k = []
        valori1 = ['Status','On/Off',str(time.time()),self.valore]
        diz = dict (zip(self.chiavi1,valori1))
        k.append(diz)
        valori = ['IOT/sensore/EmergencyButton',k]
        SenML = dict(zip(self.chiavi,valori))
        SenML_json =json.dumps(SenML)
        return SenML_json
    
    
        
        