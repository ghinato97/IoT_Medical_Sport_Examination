import json
import time
import random


class Pulsossimetro():
       
    def __init__(self):
        self.chiavi=['bn','e']
        self.chiavi1=['n','u','t','v']

    def battito(self):
        k=[]
        b=random.randint(50,154)
        valori1=['Heart rate','Bpm',str(time.time()),b]
        diz=dict(zip(self.chiavi1,valori1))
        k.append(diz)
        valori=['IOT/sensore/Heart-rate',k]
        senML=dict(zip(self.chiavi,valori))
        return(json.dumps(senML,indent=4))


    def perfusione(self):
        k=[]
        ip=round(random.uniform(0.02,20),2)
        valori1=['Perfusion','%',str(time.time()),ip]
        diz=dict(zip(self.chiavi1,valori1))
        k.append(diz)
        valori=['IOT/sensore/perfusion',k]
        senML=dict(zip(self.chiavi,valori))
        return(json.dumps(senML,indent=4))

    def saturazione(self):
        k=[]
        s=random.randint(85,99)
        valori1=['Saturation','%SpO2',str(time.time()),s]
        diz=dict(zip(self.chiavi1,valori1))
        k.append(diz)
        valori=['IOT/sensore/saturation',k]
        senML=dict(zip(self.chiavi,valori))
        return(json.dumps(senML,indent=4))

    
       



if __name__=="__main__":

    x=Pulsossimetro()
    print(x.perfusione())
    print(x.battito())
    print(x.saturazione())



          
