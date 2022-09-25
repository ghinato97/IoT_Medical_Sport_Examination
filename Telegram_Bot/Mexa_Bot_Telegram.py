from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint

# from Controllo_Emergency_Button import *
from timer import *
from threading import Thread
import random

import os
import time
import requests
import json
import cherrypy

import time 
import telepot
import pandas as pd
import matplotlib.pyplot as plt

from MyMQTT import *




class IoT_bot():
    exposed=True  
    def __init__(self):        
        
        self.flag_first=0
        self.flag_create=0
        self.flag_login=0
        self.flag_c_name=0
        self.flag_log_name=0
        self.flag_ins_patient=0
        self.flag_search_patient=0
        self.time=30
        self.flag_startsession=0
        self.flag_insert=0
        
        self.node=[1,0]
        
        f=open('Catalog.json','r')
        cat=json.load(f)   
        f.close()     
        self.Catalog_uri=cat["Catalog_uri"]

        self.dizionario=[]
        
        url=self.Catalog_uri+'/retrieve/telegramtoken'
        self.token=requests.get(url).text
        

        url=self.Catalog_uri+'/retrieve/broker'
        self.broker=requests.get(url).text

        url=self.Catalog_uri+'/retrieve/port'
        self.port=requests.get(url).text
        self.port=int(self.port)
        
        url=self.Catalog_uri+'/retrieve/ngrok'
        self.ngrok_url=requests.get(url).text
        
        url=self.Catalog_uri+'/retrieve/thingspeak_url'
        self.url_thinkspeak=requests.get(url).text
        
        
        url=self.Catalog_uri+'/retrieve/thingspeak_API'
        self.Api_User=requests.get(url).text

         
        url=self.Catalog_uri+'/retrieve/url_pub'
        self.url_pub=requests.get(url).text

        url=self.Catalog_uri+'/retrieve/topic'
        self.topic_base=requests.get(url).text
    
        url=self.Catalog_uri+'/retrieve/channels'
        r=requests.get(url).text
        self.channels=json.loads(r)
    
        
        
        
        self.bot=telepot.Bot(self.token)
        
        
        self.client= MyMQTT_("Mexa_Telegram_bot_IoT_Project", self.broker, self.port,None)
        self.client.start()
        # self.topic=self.topic_base+'/ControlEmergency'
        
        MessageLoop(self.bot, {'chat': self.handle,
                                'callback_query': self.on_callback_query}).run_as_thread()

        
        self.oudir='Data'
        if not os.path.exists(self.oudir):
            os.makedirs(self.oudir)
      
    
    def Make_Plot(self,path):
        path_csv=path+'/all_data.csv'
        data_frame=pd.read_csv(path_csv)
        time_=data_frame['created_at']
        
        
        accelerometro=data_frame['field1']
        accelerometro=accelerometro.dropna()  
        plt.figure(0)
        accelerometro_plot=accelerometro.plot()
        fig=accelerometro_plot.get_figure()
        plt.ylabel("Acceleration [rpm]")
        fig.savefig(path+'/accelerometer.png')
        plt.close()
        
        
        battito=data_frame['field2']
        battito=battito.dropna()
        plt.figure(1)
        battito_plot=battito.plot()
        fig1=battito_plot.get_figure()
        plt.ylabel("Heart Rate [bpm]")
        fig1.savefig(path+'/heart_rate.png')
        plt.close()
        

        
        saturazione=data_frame['field3']
        saturazione=saturazione.dropna()
        plt.figure(2)
        saturazione_plot=saturazione.plot()
        fig2=saturazione_plot.get_figure()
        plt.ylabel("Saturation [SpO2]")
        fig2.savefig(path+'/saturation.png')
        plt.close()
        
               

        
        perfusione=data_frame['field4']
        perfusione=perfusione.dropna()
        plt.figure(3)
        perfusione_plot=perfusione.plot()
        fig3=perfusione_plot.get_figure()
        plt.ylabel("Perfusion [%]")
        fig3.savefig(path+'/perfusion.png')
        plt.close()
        
        temperature=data_frame['field5']
        temperature=temperature.dropna()
        plt.figure(4)
        temperature_plot=perfusione.plot()
        fig4=temperature_plot.get_figure()
        plt.ylabel("Temperature [°C]")
        fig3.savefig(path+'/temperature.png')
        plt.close()

     

    def handle(self,msg):
        content_type,chat_type,chat_id=telepot.glance(msg)
        if content_type=="text":

                      
            if msg["text"]=="/start" or msg["text"]=="/logout":

                url=self.Catalog_uri+'/retrieve/allUsers'
                users=requests.get(url).text
                
            
                if len(users)==2 and self.flag_insert==0:
                  self.flag_first=1
                else:
                  self.flag_first=0 
                

                
                self.message=""
                self.create_name=""
                self.create_surname=""
                self.create_password=""
                self.log_name=""
                self.log_surname=""
                self.log_password=""
                self.nome_cognome_patiente=""
                self.nome_cognome=""
                self.nome_paziente=""
                self.surname_paziente=""
                 
                flags={"self.flag_create":self.flag_create,
                       "self.flag_login":self.flag_login,
                       "self.flag_c_name":self.flag_c_name,
                       "self.flag_log_name":self.flag_log_name,
                       "self.flag_ins_patient":self.flag_ins_patient,
                       "self.flag_time":0,
                       "self.flag_startsession":self.flag_startsession,
                       "self.flag_search_patient":self.flag_search_patient}
                 
                m={"userName":self.log_name,
                   "userSurname":self.log_surname,
                   "patient_name":self.nome_paziente,
                   "patient_surname":self.surname_paziente,
                   'chatID':chat_id,
                   'channel':0,
                   'password':0,
                   'canalenode':0,
                   'time':self.time,
                   'kit':0,
                   'timer':0,
                   "flagList":flags,
                   "path":"0"}

                if self.flag_first==0:
                  for i in range(len(self.dizionario)):
                    if self.dizionario[i]['chatID']==chat_id:
                        del self.dizionario[i]

                
                self.dizionario.append(m)
                self.flag_insert=1

            

                for i in range(len(self.dizionario)):
                  if self.dizionario[i]['chatID']==chat_id:
                      keyboard = InlineKeyboardMarkup(inline_keyboard=[
                      [InlineKeyboardButton(text=f'Login 👥', callback_data='press_login')],
                      [InlineKeyboardButton(text=f'Create New Account 📝', callback_data='press_create')]
                       ])
                      self.bot.sendMessage(chat_id, 'Welcome to MeXa 🏥\nLogin or create a new account', reply_markup=keyboard)
            
            
            #Create Account
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    if self.dizionario[i]['flagList']['self.flag_create']==1 and self.dizionario[i]['flagList']['self.flag_ins_patient']==0:
                       self.message=msg["text"]
                       self.Create_Account(chat_id)
                      
            

            #Login Account
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    x=self.dizionario[i]['flagList']
                    if x['self.flag_login']==1 and x['self.flag_ins_patient']==0:
                      self.message=msg["text"]
                      self.Login_Account(chat_id)
                      self.flag_name=1
            
            #Insert Patient
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    x=self.dizionario[i]['flagList']
                    if x['self.flag_ins_patient']==1:
                      self.message=msg["text"]
                      self.Insert_Patient(chat_id)
                      self.dizionario[i]['flagList']['self.flag_ins_patient']=0  

            # Start Session
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    x=self.dizionario[i]['flagList']
                    if x['self.flag_startsession']==1:
                      self.message=msg["text"]
                      self.start_session(chat_id)
                      self.dizionario[i]['flagList']['self.flag_startsession']=0   
                      

            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    x=self.dizionario[i]['flagList']
                    if x['self.flag_search_patient']==1:
                      self.message=msg["text"]
                      self.Search_Patient(chat_id)
                      x['self.flag_search_patient']=0
                      
                      
                      
            #settare il tempo
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    x=self.dizionario[i]['flagList']
                    if x['self.flag_time']==1:
                      self.message=msg["text"]
                      self.time=float(self.message)*60
                      self.dizionario[i]['time']=self.time                      
                      print(self.time)
                      self.dizionario[i]['time']=self.time
                      
                      if x['self.flag_login']==1:
                          
                          keyboard = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text=f'➕ Insert new patient', callback_data='insert_patient')],
                         [InlineKeyboardButton(text=f'📁 See old patient data', callback_data='old_patient')],
                         [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
                         [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
                          ])
                          
                          self.bot.sendMessage(chat_id,'✅⏱ Time setted',reply_markup=keyboard)
                          self.dizionario[i]['flagList']['self.flag_time']=0
                          
                      else:
                          keyboard = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text=f'➕ Insert new patient', callback_data='insert_patient')],
                         [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
                         [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
                          ])
                          self.bot.sendMessage(chat_id,'✅⏱ Time setted',reply_markup=keyboard)
                          self.dizionario[i]['flagList']['self.flag_time']=0
                
                              
      
     
                    
                         

            
    def on_callback_query(self,msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        
        if query_data=="press_login":
            for i in range(len(self.dizionario)):                
                if self.dizionario[i]['chatID']==chat_id:
                    self.bot.sendMessage(chat_id,text='Please insert your Name and Surname (example Mario,Rossi) 👩‍⚕️👨‍⚕️')
                    self.dizionario[i]['flagList']['self.flag_login']=1 
                                    
            
        if query_data=="press_create":            
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    self.bot.sendMessage(chat_id, text='Insert your Name and Surname (example Mario,Rossi) 👩‍⚕️👨‍⚕️')
                    self.dizionario[i]['flagList']['self.flag_create']=1


            
        if query_data=="insert_patient":
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:             
                    self.bot.sendMessage(chat_id, text='Insert Patient Name,Surname,and kit number(example Mario,Rossi,1)🏃🏃‍♀️')
                    self.dizionario[i]['flagList']['self.flag_ins_patient']=1 

              
            
        if query_data=="start_session":
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:  
                    
                    self.bot.answerCallbackQuery(query_id,text='⏳ Session started ,please attend ⏳\nOnline data available at the link')     
                    self.bot.sendMessage(chat_id, self.ngrok_url+'/#!/'+str(self.dizionario[i]['canalenode']), disable_web_page_preview=False) 
                    
                    channel=self.dizionario[i]['channel']                        
                    tempo=self.dizionario[i]['time']
                    t=str(tempo)                    
    
        
                    url=self.url_pub+'/pub/'+str(channel)+'/'+str(self.dizionario[i]['kit'])+'/'+t
                    print(url)
                    r=requests.get(url)
                    
                    
                    self.dizionario[i]['timer']=time.time()
                    
                    message={'chat_id':chat_id,
                             'tempo':tempo}
                    

                    session_thread_=Thread(target=Timer)
                    session_thread_.start()

                    time.sleep(3)
                    self.client.myPublish('timer/mexa', message)

                    
                  
                    
                  
                
                    
        if query_data=="data_plot":
            for i in range(len(self.dizionario)):
             if self.dizionario[i]['chatID']==chat_id:
                 path=self.dizionario[i]['path']
                 self.bot.sendPhoto(chat_id,open(path+'/accelerometer.png','rb'))
                 self.bot.sendPhoto(chat_id,open(path+'/heart_rate.png','rb'))
                 self.bot.sendPhoto(chat_id,open(path+'/saturation.png','rb'))
                 self.bot.sendPhoto(chat_id,open(path+'/perfusion.png','rb'))
                 
                 keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
                [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
                 ])
                 self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
                 
                 
             
        
        if query_data=='heart_plot':
            for i in range(len(self.dizionario)):
             if self.dizionario[i]['chatID']==chat_id:
                 path=self.dizionario[i]['path']
                 self.bot.sendPhoto(chat_id,open(path+'/heart_rate.png','rb'))
                 keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
                [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
                 ])
                 self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
                
        
        if query_data=='pulso_plot':
            for i in range(len(self.dizionario)):
             if self.dizionario[i]['chatID']==chat_id:
                 path=self.dizionario[i]['path']
                 self.bot.sendPhoto(chat_id,open(path+'/perfusion.png','rb'))
                 keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
                [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
                 ])
                 self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
             
        if query_data=='satu_plot':
            for i in range(len(self.dizionario)):
             if self.dizionario[i]['chatID']==chat_id:
                 path=self.dizionario[i]['path']
                 self.bot.sendPhoto(chat_id,open(path+'/saturation.png','rb'))
                 keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
                [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
                 ])
                 self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='acc_plot':
            for i in range(len(self.dizionario)):
             if self.dizionario[i]['chatID']==chat_id:
                 path=self.dizionario[i]['path']
                 self.bot.sendPhoto(chat_id,open(path+'/accelerometer.png','rb'))
                 keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
                [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
                 ])
                 self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
        
        if query_data=='temp_plot':
            for i in range(len(self.dizionario)):
             if self.dizionario[i]['chatID']==chat_id:
                 path=self.dizionario[i]['path']
                 self.bot.sendPhoto(chat_id,open(path+'/temperature.png','rb'))
                 keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'🔙', callback_data='back_data_plot')], 
                [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')]
                 ])
                 self.bot.sendMessage(chat_id, 'Choose one', reply_markup=keyboard)
                
        if query_data=='back_data_plot':
            for i in range(len(self.dizionario)):
             if self.dizionario[i]['chatID']==chat_id:
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
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    
                    self.flag_first=0
                    self.flag_create=0
                    self.flag_login=0
                    self.flag_c_name=0
                    self.flag_log_name=0
                    self.flag_ins_patient=0
                    self.flag_search_patient=0
                    self.flag_time=0
                    self.flag_startsession=0
                    
                    flags={"self.flag_create":self.flag_create,
                           "self.flag_login":self.flag_login,
                           "self.flag_c_name":self.flag_c_name,
                           "self.flag_log_name":self.flag_log_name,
                           "self.flag_ins_patient":self.flag_ins_patient,
                           "self.flag_time":self.flag_time,
                           "self.flag_startsession":self.flag_startsession,
                           "self.flag_search_patient":self.flag_search_patient}
                    
                    self.dizionario[i]['flags']=flags
                        
           
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text=f'Login 👥', callback_data='press_login')],
           [InlineKeyboardButton(text=f'Create New Account 📝', callback_data='press_create')]
               ])
            self.bot.sendMessage(chat_id, 'Welcome to MeXa 🏥\nLogin or create a new account', reply_markup=keyboard)
        
        if query_data=='back':
          for i in range(len(self.dizionario)):
            if self.dizionario[i]['chatID']==chat_id:
             testo="Welcome "+self.dizionario[i]['userName']
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
            for i in range(len(self.dizionario)):
                if self.dizionario[i]['chatID']==chat_id:
                    self.dizionario[i]['flagList']['self.flag_search_patient']=1

            
        
        if query_data=='set_time':
            for i in range(len(self.dizionario)):
                self.bot.sendMessage(chat_id,'⏳ Insert session length (in minute)') 
                if self.dizionario[i]['chatID']==chat_id:
                    self.dizionario[i]['flagList']['self.flag_time']=1
        
    
    
    def Create_Account(self,chat_id):        
        for i in range(len(self.dizionario)):
          if self.dizionario[i]['chatID']==chat_id:              
            l=self.dizionario[i]['flagList']
            if l['self.flag_c_name']==0:
               self.dizionario[i]['flagList']['self.flag_c_name']=1
               x=self.message.split(",")
               if len(x)==2:
                self.dizionario[i]['userName']=x[0]
                self.dizionario[i]['userSurname']=x[1]
                self.bot.sendMessage(chat_id, text='Insert your password🔐')
                self.log_name=self.dizionario[i]['userName']
                self.log_surname=self.dizionario[i]['userSurname']
                print(self.log_name)
                print(self.log_surname)
            else:
              self.create_password=self.message
              self.dizionario[i]['password']=self.create_password

            
              url=self.Catalog_uri+'/add/user'        
              chiavi=["userName","userSurname","password",'chat_ID',"patientList"]
              val=[ self.dizionario[i]['userName'],self.dizionario[i]['userSurname'],self.dizionario[i]['password'],self.dizionario[i]['chatID']]    
              dizionario = dict(zip(chiavi,val))        
              r=requests.post(url,json=dizionario)
             
              nome_cognome=self.dizionario[i]['userName'] +'_'+ self.dizionario[i]['userSurname']
              if not os.path.exists(os.path.join(self.oudir,nome_cognome)):
                  os.makedirs(os.path.join(self.oudir,nome_cognome))
              
     
              self.dizionario[i]['flagList']['self.flag_create']=0

              self.dizionario[i]['flagList']['self.flag_c_name']=0
    
              testo="✅Account Created!\nWelcome "+self.dizionario[i]['userName']
              
              keyboard = InlineKeyboardMarkup(inline_keyboard=[
                 [InlineKeyboardButton(text=f'➕ Insert new Patient', callback_data='insert_patient')],
                 [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
                 [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
                 ])
              self.bot.sendMessage(chat_id, testo, reply_markup=keyboard)
            
        
    def Login_Account(self,chat_id):                  
          url=self.Catalog_uri+'/retrieve/allUsers'
          Userlist=requests.get(url).json()
            
          self.flag_errore_log=0    
          for i in range(len(self.dizionario)):
            if self.dizionario[i]['chatID']==chat_id:
              
              if self.dizionario[i]['flagList']['self.flag_log_name']==0:
                self.dizionario[i]['flagList']['self.flag_log_name']=1
                x=self.message.split(",")
                if len(x)==2:
                  self.dizionario[i]['userName']=x[0]
                  self.dizionario[i]['userSurname']=x[1]
                  self.bot.sendMessage(chat_id,text='Insert your password 🔐')
                  nome_cognome=self.dizionario[i]['userName']+'_'+self.dizionario[i]['userSurname']
                  print(self.log_name)
                  print(self.log_surname)
              else:            
                 self.log_password=self.message
                 self.dizionario[i]['password']=self.log_password

                
                 self.dizionario[i]['flagList']['self.flag_log_name']=0
                 self.dizionario[i]['flagList']['self.flag_login']=0
                  
                 for k in range(len(Userlist)):
                    if Userlist[k]['Name']==self.dizionario[i]['userName'] and Userlist[k]['Surname']==self.dizionario[i]['userSurname'] and Userlist[k]['password']==(self.dizionario[i]['password']):
                        testo="Welcome "+self.dizionario[i]['userName']
                        self.flag_errore_log=1
                        
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f'➕ Insert new patient', callback_data='insert_patient')],
                        [InlineKeyboardButton(text=f'📁 See old patient data', callback_data='old_patient')],
                        [InlineKeyboardButton(text=f'⏱ Set time', callback_data='set_time')],
                        [InlineKeyboardButton(text=f'⭕️ Log out', callback_data='log_out')],
                            ])
                        self.bot.sendMessage(chat_id,'✅'+ testo , reply_markup=keyboard)
                 if self.flag_errore_log==0:                
                      keyboard = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text=f'Login 👥', callback_data='press_login')],
                     [InlineKeyboardButton(text=f'Create New Account 📝', callback_data='press_create')]
                      ])
                      self.bot.sendMessage(chat_id, "❌ errore credenziali ❌", reply_markup=keyboard)
                
    def Insert_Patient(self,chat_id): 
    
        x=self.message.split(",")
        for i in range(len(self.dizionario)):
                 
          if self.dizionario[i]['chatID']==chat_id:
            
            self.patient_name=x[0]
            self.dizionario[i]['patient_name']=self.patient_name
            
            self.patient_surname=x[1]
            self.dizionario[i]['patient_surname']=self.patient_surname
            
            self.dizionario[i]['kit']=x[2]
            kit=str(x[2])
            
            self.dizionario[i]['flagList']['self.flag_ins_patient']=0
            
            url=self.Catalog_uri+'/add/patient'
            
            if len(self.channels)!=0:
                
                canale= self.channels.pop()
                self.dizionario[i]['channel']=canale
                canalenode=self.node.pop()
                self.dizionario[i]['canalenode']=canalenode

    
                patient_surname=self.dizionario[i]['patient_surname']
                patient_name=self.dizionario[i]['patient_name']
                
                nome_cognome =self.dizionario[i]['userName'] +'_'+ self.dizionario[i]['userSurname']
                nome_cognome_patiente=self.dizionario[i]['patient_name']+'_'+self.dizionario[i]['patient_surname']
                
                if not os.path.exists(os.path.join(self.oudir,nome_cognome,nome_cognome_patiente)):
                    os.makedirs(os.path.join(self.oudir,nome_cognome,nome_cognome_patiente))
                    
                self.dizionario[i]['path']=os.path.join(self.oudir,nome_cognome,nome_cognome_patiente)
                
                    
                payload={'User_name':self.dizionario[i]['userName'],'User_surname':self.dizionario[i]['userSurname'],'Patient_name':self.dizionario[i]['patient_name'],'Patient_surname':self.dizionario[i]['patient_surname']}
                r=requests.post(url,params=payload,json=payload)
                
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'🟢 Start Session', callback_data='start_session')],
                [InlineKeyboardButton(text=f'🔙', callback_data='back')]
                    ])
                self.bot.sendMessage(chat_id,text= 'Select',reply_markup=keyboard)  
            
            else:
                self.bot.sendMessage(chat_id,text= 'Canali non disponibili al momento')  

        
        
        
    def Search_Patient(self,chat_id):
           x=self.message.split(",")
           for i in range(len(self.dizionario)):
            if self.dizionario[i]['chatID']==chat_id:
                
                self.dizionario[i]['patient_name']=x[0]
                self.dizionario[i]['patient_surname']=x[1]
                
                nome_cognome =self.dizionario[i]['userName'] +'_'+ self.dizionario[i]['userSurname']
                nome_cognome_patiente=self.dizionario[i]['patient_name']+'_'+self.dizionario[i]['patient_surname']
                self.path=os.path.join(self.oudir,self.dizionario[i]['userSurname'] +'_'+ self.dizionario[i]['userName'],nome_cognome_patiente)
                if not os.path.exists(os.path.join(self.oudir,nome_cognome,nome_cognome_patiente)):
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
                
 
    def start(self):
        self.client_.start()
       
                    
    def GET(self,*uri,**params):            
            if len(uri)!=0:
                
                if uri[0]=='Emergency':
                  kit=uri[1]
                  for i in range(len(self.dizionario)):
                        if self.dizionario[i]['kit']==kit:
                          self.bot.sendMessage(self.dizionario[i]['chatID'], '⚠️⚠️⚠️ Patient pushed the emergency button , please check !')
                          
                if uri[0]=='Session_End':
                    print('session end')
                    chat_id=int(uri [1])
                    for i in range(len(self.dizionario)):
                        if self.dizionario[i]['chatID']==chat_id:
                            tempo_inizio=self.dizionario[i]['timer']
                            
                            channel=self.dizionario[i]['channel']
                            self.channels.append(channel)
                            self.node.append(self.dizionario[i]['canalenode'])
                         
                         
                            url=self.url_thinkspeak+ str(channel)+'/feeds.csv'
                            r=requests.get(url)
                        
                            nome_cognome =self.dizionario[i]['userName'] +'_'+ self.dizionario[i]['userSurname']
                            nome_cognome_patiente=self.dizionario[i]['patient_name']+'_'+self.dizionario[i]['patient_surname']
                            
                            path=os.path.join(self.oudir,nome_cognome,nome_cognome_patiente)
                            with open(path+'/all_data.csv','w') as file:
                                  file.write(r.text)
                         
                            self.Make_Plot(path) 
                        
                            url=self.url_thinkspeak+str(channel)+'/feeds.json'
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
                            return str('ok')
                    else:
                        return(str('errore chat id'))

                    
                    
                
                     
                 
                 


if __name__=="__main__":
    b=IoT_bot()
    print('Bot working')
    conf = {
                '/': {
                        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                        'tools.sessions.on': True
                }
        }
    cherrypy.tree.mount(b, '/', conf) 
    cherrypy.config.update({'server.socket_port': 8094})
    cherrypy.engine.start()

    cherrypy.engine.block()

    while True:
        
        time.sleep(1)

