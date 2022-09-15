from MyMQTT import *
import telepot
import time

class Controllo_emergency:
    def __init__(self,chat_ID):
        conf=json.load(open("Catalog.json",'r'))
        broker=conf["broker"]['IpAddress']
        port=conf["broker"]['port']
        token=conf['telegramToken']
        clientID='Control_Emergency_Button'
        self.topic_but='IoT_Polito_Project/Sensor/Emergency'
        self.chat_ID=chat_ID
        
        self.client=MyMQTT_(clientID,broker,port,self)
        
        self.bot=telepot.Bot(token)
    
    def start(self):
        self.client.start()
        self.client.mySubscribe(self.topic_but)
    
    def stop(self):
        self.client.stop()
        
    def notify(self,topic,msg):
        messaggio=json.loads(msg)
        valore=messaggio['e'][0]['v']
        if valore==1:
            self.bot.sendMessage(self.chat_ID,text='⚠️⚠️⚠️ Patient pushed the emergency button , please check !')
            
            
            
if __name__=="__main__":
    x=Controllo_emergency('elios')
    time.sleep(1)
    x.start()