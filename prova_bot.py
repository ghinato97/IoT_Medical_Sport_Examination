
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
from All_sensor_MQTT_TS_PUB import *
from Make_Plot_Telegram import *
from threading import Thread
import os
import time
import requests
import json
import time 
import telepot


class IoT_bot():
    def __init__(self,token,channelID):        
        self.bot=telepot.Bot(token)
        # MessageLoop(self.bot,self.handle).run_as_thread()
        MessageLoop(self.bot, {'chat': self.handle,
                               'callback_query': self.on_callback_query}).run_as_thread()
        
        self.flag_create=0
        self.flag_login=0
        self.flag_c_name=0
        self.flag_log_name=0
        self.flag_ins_patient=0
        self.channelID=channelID

        
        # f=open('Catalog.json','r')
        # cat=json.load(f)   
        # self.Userlist=cat['usersList']
        self.oudir='Data'
        if not os.path.exists(self.oudir):
            os.makedirs(self.oudir)
        
    def prova(self):
        pprint(self.bot.getMe())
    
    def handle(self,msg):
        content_type,chat_type,chat_id=telepot.glance(msg)
        if content_type=="text":
            if msg["text"]=="/start":
                               
                self.flag_create=0
                self.flag_login=0
                self.flag_c_name=0
                self.flag_log_name=0
                self.flag_ins_patient=0
                
                self.message=""
                self.create_name=""
                self.create_surname=""
                self.create_password=""
                self.log_name=""
                self.log_surname=""
                self.log_password=""
                self.nome_cognome_patiente=""
                self.nome_cognome=""
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
               [InlineKeyboardButton(text=f'Login 🔓', callback_data='press_login')],
               [InlineKeyboardButton(text=f'Create New Account 📝', callback_data='press_create')]
                   ])
                self.bot.sendMessage(chat_id, 'Welcome to MeXa, login or create a new account', reply_markup=keyboard)
            
                
            if self.flag_create==1 and self.flag_ins_patient==0:
                self.message=msg["text"]
                self.Create_Account(chat_id)
                self.flag_name=1
            
            if self.flag_login==1 and self.flag_ins_patient==0:
                self.message=msg["text"]
                self.Login_Account(chat_id)
                self.flag_name=1
                         
            if self.flag_ins_patient==1:
                self.message=msg["text"]
                self.Insert_Patient(chat_id)


                
    def on_callback_query(self,msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        if query_data=="press_login":
            self.bot.sendMessage(chat_id,text='Insert your Name and Surname (example Mario,Rossi)')
            self.flag_login=1
        if query_data=="press_create":
            self.bot.sendMessage(chat_id, text='Insert your Name and Surname (example Mario,Rossi)')
            self.flag_create=1
        if query_data=="insert_patient":
            self.bot.sendMessage(chat_id, text='Insert Patient Name ')
            self.flag_ins_patient=1
        if query_data=="start_session":
            self.bot.sendMessage(chat_id, text='Session started ,please attend')
            x=Sensors_Run()
            session_thread = Thread(target=x.publish())
            session_thread.start()
            session_thread.join()
            self.bot.sendMessage(chat_id, text='Session ended')
            
            url='https://api.thingspeak.com/channels/'+ str(self.channelID)+'/feeds.csv'
            r=requests.get(url)
            self.path=os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente)
            with open(self.path+'/all_data.csv','w') as file:
                file.write(r.text)
                
            Make_Plot(self.path)
                
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'Show Data plot', callback_data='data_plot')]])
            self.bot.sendMessage(chat_id, 'Che facciamo?', reply_markup=keyboard)
         
        if query_data=="data_plot":
            self.bot.sendPhoto(chat_id,open(self.path+'/accelerometer.png','rb'))
            self.bot.sendPhoto(chat_id,open(self.path+'/heart_rate.png','rb'))
            self.bot.sendPhoto(chat_id,open(self.path+'/saturation.png','rb'))
            self.bot.sendPhoto(chat_id,open(self.path+'/perfusion.png','rb'))
     
                
          

            
            
    
    def Create_Account(self,chat_id):
        if self.flag_c_name==0:
            self.flag_c_name=1
            x=self.message.split(",")
            if len(x)==2:
                self.log_name=x[0]
                self.log_surname=x[1]
                self.bot.sendMessage(chat_id, text='Insert your password')
                print(self.log_name)
                print(self.log_surname)
        else:
            self.create_password=self.message
            print(self.log_password)
            
            url='http://127.0.0.1:8090/add/user'        
            chiavi=["userName","userSurname","password","patientList"]
            val=[self.log_name,self.log_surname,self.create_password]    
            dizionario = dict(zip(chiavi,val))        
            r=requests.post(url,json=dizionario)
            
            
            self.nome_cognome=self.log_surname +'_'+ self.log_name
            if not os.path.exists(os.path.join(self.oudir,self.nome_cognome)):
                os.makedirs(os.path.join(self.oudir,self.nome_cognome))
            
            
            self.flag_create=0
            self.flag_c_name=0
            
            testo="Welcome "+self.create_name
            self.bot.sendMessage(chat_id, text=testo)
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'New Patient', callback_data='insert_patient')]])
            self.bot.sendMessage(chat_id, 'Che facciamo?', reply_markup=keyboard)
            
        
    def Login_Account(self,chat_id):
                
        f=open('Catalog.json','r')
        cat=json.load(f)   
        self.Userlist=cat['usersList']
        flag_errore_log=0        
        if self.flag_log_name==0:
            
            self.flag_log_name=1
            x=self.message.split(",")
            if len(x)==2:
                self.log_name=x[0]
                self.log_surname=x[1]
                self.bot.sendMessage(chat_id,text='Insert your password')
                self.nome_cognome=self.log_surname +'_'+ self.log_name
                print(self.log_name)
                print(self.log_surname)
        else:            
            self.log_password=self.message
            print(self.log_password)
            
            self.flag_login=0
            self.flag_log_name=0
                
            for i in range(len(self.Userlist)):
                if self.Userlist[i]['Name']==self.log_name and self.Userlist[i]['Surname']==self.log_surname and self.Userlist[i]['password']==self.log_password:
                    testo="Welcome "+self.log_name
                    self.bot.sendMessage(chat_id,text=testo)
                    flag_errore_log=1
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text=f'New Patient', callback_data='insert_patient')],
                   [InlineKeyboardButton(text=f' Old Patient', callback_data='old_patient')]
                       ])
                    self.bot.sendMessage(chat_id, 'Che facciamo?', reply_markup=keyboard)
            if flag_errore_log==0:
                self.bot.sendMessage(chat_id,text="errore credenziali")
                
    def Insert_Patient(self,chat_id): 
    
        x=self.message.split(",")
        self.patient_name=x[0]
        self.patient_surname=x[1]
        self.flag_ins_patient=0
        url='http://127.0.0.1:8090/add/patient'
        print(self.log_name)
        print(self.log_surname)
        
        self.nome_cognome_patiente=self.patient_surname+'_' + self.patient_name
        if not os.path.exists(os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente)):
            os.makedirs(os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente))
        
        
        
        payload={'User_name':self.log_name,'User_surname':self.log_surname,'Patient_name':self.patient_name,'Patient_surname':self.patient_surname}
        r=requests.post(url,params=payload,json=payload)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Start Session', callback_data='start_session')],
        [InlineKeyboardButton(text=f' Back', callback_data='back')]
            ])
        self.bot.sendMessage(chat_id, 'Che facciamo?', reply_markup=keyboard)
        
        
        
        
            
                    
                    
                    
                    


if __name__=="__main__":
    conf=json.load(open("Catalog.json"))
    token=conf['telegramToken']
    channelID=conf['thingSpeak']['channelID']
    b=IoT_bot(token,channelID)
    print('Bot working')
    while True:
        time.sleep(1)
        
