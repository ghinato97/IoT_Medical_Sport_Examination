import numpy as np
import json
import time
import random

class EmergencyButton:
    
    
    def __init__(self):
    
        self.chiavi = ['bn','e']
        self.chiavi1 = ['n','u','t','v']
        
    def Button(self):
        k = []
        n=1
        valori1 = ['Status','Status',str(time.time()),1]
        diz = dict (zip(self.chiavi1,valori1))
        k.append(diz)
        valori = ['IOT/sensore/EmergencyButton',k]
        SenML = dict(zip(self.chiavi,valori))
        SenML_json =json.dumps(SenML)
        return SenML_json
    