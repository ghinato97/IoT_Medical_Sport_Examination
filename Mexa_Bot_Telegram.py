
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
from All_sensor_MQTT_TS_PUB import *
from Make_Plot_Telegram import *
from Controllo_Emergency_Button import *
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
        MessageLoop(self.bot, {'chat': self.handle,
                               'callback_query': self.on_callback_query}).run_as_thread()
        
        self.flag_create=0
        self.flag_login=0
        self.flag_c_name=0
        self.flag_log_name=0
        self.flag_ins_patient=0
        self.flag_search_patient=0
        self.channelID=channelID
        
        
        f=open('Catalog.json','r')
        cat=json.load(f)   
        f.close()     
        self.Api_User=cat["thingSpeak"]["User_Api"]
        self.Catalog_uri=cat["Catalog_uri"]
        self.url_pub=cat['url_pub']
        self.url_temp=cat['url_temp']
        self.ngrok_url=cat['Ngrok_url']
        
        
        self.oudir='Data'
        if not os.path.exists(self.oudir):
            os.makedirs(self.oudir)
        
    def prova(self):
        pprint(self.bot.getMe())
    
    def handle(self,msg):
        content_type,chat_type,chat_id=telepot.glance(msg)
        if content_type=="text":
            if msg["text"]=="/start" or msg["text"]=="/logout":
                               
                self.flag_create=0
                self.flag_login=0
                self.flag_c_name=0
                self.flag_log_name=0
                self.flag_ins_patient=0
                self.flag_time=0
                self.time=30
                
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
               [InlineKeyboardButton(text=f'Login 👥', callback_data='press_login')],
               [InlineKeyboardButton(text=f'Create New Account 📝', callback_data='press_create')]
                   ])
                self.bot.sendMessage(chat_id, 'Welcome to MeXa 🏥\nLogin or create a new account', reply_markup=keyboard)
            
                
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
            
            if self.flag_search_patient==1:
                self.message=msg["text"]
                self.Search_Patient(chat_id)
                self.flag_search_patient=0
            
            if self.flag_time==1:
                self.message=msg["text"]
                self.time=float(self.message)*60
                print(self.time)
                if self.flag_login==1:
                     keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=f'➕ Insert new patient', callback_data='insert_patient')],
                    [InlineKeyboardButton(text=f'📁 See old patient data', callback_data='old_patient')],
                    [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
                    [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
                        ])
                     self.bot.sendMessage(chat_id,'✅⏱ Time setted',reply_markup=keyboard)
                     self.flag_time=0
                else:
                     keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=f'➕ Insert new patient', callback_data='insert_patient')],
                    [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
                    [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
                        ])
                     self.bot.sendMessage(chat_id,'✅⏱ Time setted',reply_markup=keyboard)
                     self.flag_time=0
                    
                         


                
    def on_callback_query(self,msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        
        if query_data=="press_login":
            self.bot.sendMessage(chat_id,text='Please insert your Name and Surname (example Mario,Rossi) 👩‍⚕️👨‍⚕️')
            self.flag_login=1
            
            
        if query_data=="press_create":
            self.bot.sendMessage(chat_id, text='Insert your Name and Surname (example Mario,Rossi) 👩‍⚕️👨‍⚕️')
            self.flag_create=1
            
            
        if query_data=="insert_patient":
            self.bot.sendMessage(chat_id, text='Insert Patient Name and Surname (example Mario,Rossi)🏃🏃‍♀️')
            self.flag_ins_patient=1
            
            
        if query_data=="start_session":
            self.bot.answerCallbackQuery(query_id,text='⏳ Session started ,please attend ⏳\nOnline data available at the link')
            self.bot.sendMessage(chat_id, self.ngrok_url, disable_web_page_preview=False)
            
            id_chat=str(chat_id)
            x=Controllo_emergency(chat_id)
            session_thread_=Thread(target=x.start())
            session_thread_.start()
            

            
            t=str(self.time)
            url=self.url_pub+'/pub/'+t
            r=requests.get(url)
            
            session_thread_.join(3)

            
            
            #richiedo il file csv con tutti i dati
            url='https://api.thingspeak.com/channels/'+ str(self.channelID)+'/feeds.csv'
            r=requests.get(url)
            
            self.path=os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente)
            with open(self.path+'/all_data.csv','w') as file:
                file.write(r.text)
          
            Make_Plot(self.path)   
            
            #elimino i dati da ThingSpeak
            url='https://api.thingspeak.com/channels/'+ str(self.channelID)+'/feeds.json'          
            parametri={"apikey":self.Api_User}
            r=requests.delete(url,params=parametri)
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
          [InlineKeyboardButton(text=f'📊 All Data plot', callback_data='data_plot')],
          [InlineKeyboardButton(text=f'🫀 Heart Rate plot', callback_data='heart_plot')],
          [InlineKeyboardButton(text=f'〰️ Perfusion plot', callback_data='pulso_plot')],        
          [InlineKeyboardButton(text=f'🩸Saturation plot', callback_data='satu_plot')],
          [InlineKeyboardButton(text=f'🏃🏽‍♂️ Accelerometer plot', callback_data='acc_plot')], 
          [InlineKeyboardButton(text=f'🌡 Temperature plot', callback_data='temp_plot')], 
          [InlineKeyboardButton(text=f'🔙', callback_data='back')]
            ])
            self.bot.sendMessage(chat_id, 'Session Complete !', reply_markup=keyboard)
            
                   
             

         


            
            
         
        if query_data=="data_plot":
            self.bot.sendPhoto(chat_id,open(self.path+'/accelerometer.png','rb'))
            self.bot.sendPhoto(chat_id,open(self.path+'/heart_rate.png','rb'))
            self.bot.sendPhoto(chat_id,open(self.path+'/saturation.png','rb'))
            self.bot.sendPhoto(chat_id,open(self.path+'/perfusion.png','rb'))
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
            ])
            self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='heart_plot':
            self.bot.sendPhoto(chat_id,open(self.path+'/heart_rate.png','rb'))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
            ])
            self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='pulso_plot':
            self.bot.sendPhoto(chat_id,open(self.path+'/perfusion.png','rb'))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
            ])
            self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='satu_plot':
            self.bot.sendPhoto(chat_id,open(self.path+'/saturation.png','rb'))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
            ])
            self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='acc_plot':
            self.bot.sendPhoto(chat_id,open(self.path+'/accelerometer.png','rb'))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
            ])
            self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='temp_plot':
            self.bot.sendPhoto(chat_id,open(self.path+'/temperature.png','rb'))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
            ])
            self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='back_data_plot':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'📊 All Data plot', callback_data='data_plot')],
           [InlineKeyboardButton(text=f'🫀 Heart Rate plot', callback_data='heart_plot')],
           [InlineKeyboardButton(text=f'〰️ Perfusion plot', callback_data='pulso_plot')],        
           [InlineKeyboardButton(text=f'🩸Saturation plot', callback_data='satu_plot')],
           [InlineKeyboardButton(text=f'🏃🏽‍♂️ Accelerometer plot', callback_data='acc_plot')], 
           [InlineKeyboardButton(text=f'🌡 Temperature plot', callback_data='temp_plot')], 
           [InlineKeyboardButton(text=f'🔙', callback_data='back')]
            ])
            self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
            
       
            
            
            
            
            
        
        if query_data=='log_out':
            self.flag_create=0
            self.flag_login=0
            self.flag_c_name=0
            self.flag_log_name=0
            self.flag_ins_patient=0
            self.flag_search_patient=0
            self.flag_time=0
            
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
           [InlineKeyboardButton(text=f'Login 👥', callback_data='press_login')],
           [InlineKeyboardButton(text=f'Create New Account 📝', callback_data='press_create')]
               ])
            self.bot.sendMessage(chat_id, 'Welcome to MeXa 🏥\nLogin or create a new account', reply_markup=keyboard)
        
        if query_data=='back':
            testo="Welcome "+self.log_name
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'➕ Insert new patient', callback_data='insert_patient')],
           [InlineKeyboardButton(text=f'📁 See old patient data', callback_data='old_patient')],
           [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
               ])
            self.bot.sendMessage(chat_id,'✅'+ testo , reply_markup=keyboard)
        
        
        if query_data=='old_patient':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔎 Search Patient', callback_data='search_patient')],
           [InlineKeyboardButton(text=f'🔙', callback_data='back')]
               ])
            self.bot.sendMessage(chat_id,'Choose one' , reply_markup=keyboard)
            
        if query_data=='search_patient':
            self.bot.sendMessage(chat_id,'Insert patient Name and Surname (example Mario,Rossi)')
            self.flag_search_patient=1
        
        if query_data=='set_time':
            self.bot.sendMessage(chat_id,'⏳ Insert session length (in minute)')
            self.flag_time=1
            
    
    
    def Create_Account(self,chat_id):
        if self.flag_c_name==0:
            self.flag_c_name=1
            x=self.message.split(",")
            if len(x)==2:
                self.log_name=x[0]
                self.log_surname=x[1]
                self.bot.sendMessage(chat_id, text='Insert your password🔐')
                print(self.log_name)
                print(self.log_surname)
        else:
            self.create_password=self.message
            print(self.log_password)
            
            url=self.Catalog_uri+'/add/user'        
            chiavi=["userName","userSurname","password","patientList"]
            val=[self.log_name,self.log_surname,self.create_password]    
            dizionario = dict(zip(chiavi,val))        
            r=requests.post(url,json=dizionario)
            
            
            self.nome_cognome=self.log_surname +'_'+ self.log_name
            if not os.path.exists(os.path.join(self.oudir,self.nome_cognome)):
                os.makedirs(os.path.join(self.oudir,self.nome_cognome))
            
            
            self.flag_create=0
            self.flag_c_name=0
            
            testo="✅Account Created!\nWelcome "+self.log_name
           
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'➕ Insert new Patient', callback_data='insert_patient')],
           [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
           [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
           ])
            self.bot.sendMessage(chat_id, testo, reply_markup=keyboard)
            
        
    def Login_Account(self,chat_id):
                
        f=open('Catalog.json','r')
        cat=json.load(f)   
        f.close()        
        self.Userlist=cat['usersList']
        flag_errore_log=0        
        if self.flag_log_name==0:
            
            self.flag_log_name=1
            x=self.message.split(",")
            if len(x)==2:
                self.log_name=x[0]
                self.log_surname=x[1]
                self.bot.sendMessage(chat_id,text='Insert your password 🔐')
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
                    flag_errore_log=1
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text=f'➕ Insert new patient', callback_data='insert_patient')],
                   [InlineKeyboardButton(text=f'📁 See old patient data', callback_data='old_patient')],
                   [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
                   [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
                       ])
                    self.bot.sendMessage(chat_id,'✅'+ testo , reply_markup=keyboard)
            if flag_errore_log==0:                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
               [InlineKeyboardButton(text=f'Login 👥', callback_data='press_login')],
               [InlineKeyboardButton(text=f'Create New Account 📝', callback_data='press_create')]
                   ])
                self.bot.sendMessage(chat_id, "❌ errore credenziali ❌", reply_markup=keyboard)
                
    def Insert_Patient(self,chat_id): 
    
        x=self.message.split(",")
        self.patient_name=x[0]
        self.patient_surname=x[1]
        self.flag_ins_patient=0
        url=self.Catalog_uri+'/add/patient'

        
        self.nome_cognome_patiente=self.patient_surname+'_' + self.patient_name
        if not os.path.exists(os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente)):
            os.makedirs(os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente))
        
        
        
        payload={'User_name':self.log_name,'User_surname':self.log_surname,'Patient_name':self.patient_name,'Patient_surname':self.patient_surname}
        r=requests.post(url,params=payload,json=payload)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'🟢 Start Session', callback_data='start_session')],
        [InlineKeyboardButton(text=f'🔙', callback_data='back')]
            ])
        self.bot.sendMessage(chat_id,text= 'Select',reply_markup=keyboard)    
    
    def Search_Patient(self,chat_id):
        x=self.message.split(",")
        self.patient_name=x[0]
        self.patient_surname=x[1]
        self.nome_cognome_patiente=self.patient_surname+'_' + self.patient_name
        self.path=os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente)
        if not os.path.exists(os.path.join(self.oudir,self.nome_cognome,self.nome_cognome_patiente)):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'🔎 Search Patient', callback_data='search_patient')],
           [InlineKeyboardButton(text=f'🔙', callback_data='back')],
               ])
            self.bot.sendMessage(chat_id,text= 'Patient not found',reply_markup=keyboard)   
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'📊 All Data plot', callback_data='data_plot')],
           [InlineKeyboardButton(text=f'🫀 Heart Rate plot', callback_data='heart_plot')],
           [InlineKeyboardButton(text=f'〰️ Perfusion plot', callback_data='pulso_plot')],        
           [InlineKeyboardButton(text=f'🩸Saturation plot', callback_data='satu_plot')],
           [InlineKeyboardButton(text=f'🏃🏽‍♂️ Accelerometer plot', callback_data='acc_plot')], 
           [InlineKeyboardButton(text=f'🔙', callback_data='back')]
            ])
            self.bot.sendMessage(chat_id, '✅ Patient found', reply_markup=keyboard)
    
        
        
        
        
            
                    
                    
                    
                    


if __name__=="__main__":
    conf=json.load(open("Catalog.json"))
    token=conf['telegramToken']
    channelID=conf['thingSpeak']['channelID']
    b=IoT_bot(token,channelID)
    print('Bot working')
    while True:
        time.sleep(1)
        
