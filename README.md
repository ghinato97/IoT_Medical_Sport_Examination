# Table of Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Set-up](#set-up)


## General Info
This is a repository for a IoT projectca calle Mexa (Medical sport (tele) Examination.
The proposed IoT platform aims at monitoring vital signs of the patient under stress condition during a sports medical examination in remote mode. 
It integrates different IoT devices that provides us patient’s data such as:
- Pulse Rate
- Respiration Rate
- Saturation
- Perfusion
- Rpm
- Also the patient can switch an emergency button if an emergency occurs

Three leds are employed to guarantee a communication between the doctor and the patient. 
The big red led is used to warn the patient that the session has started by switching it on, the opposite happen for session end.  Two small leds, green and red, are employed to communicate to the patient that his acceleration has to be increased, while green led blinking, or reduced, while the red blinking. 
The doctor can access real time monitoring of the sensors using the Telegram Bot which provides a link for the 
node-red dashboard. At the end of the session he can choose to see the data plotting of the sensors for the entire session. All data sensors are stored during the session using Thingspeak. Multiple sessions cannot run simultaneously. 

MeXa IoT Platform - Promo Video
https://www.youtube.com/watch?v=hCprphnRJ3k

MeXa IoT Platform - Demo Video
https://www.youtube.com/watch?v=tMEbXAjwmAI

## Technologies
The project is created using:
- Rasperry Pi 2 (led, and a button; all the other sensors are simulated but you can integrate in your code)
- Python 3
- Node-red
- Thingspeak
- Ngrok
- Telegram

 ![Project Scheme](IoT_Medical_Sport_Examination/image/)



## Set-up
At first is mandatory to create a Telegram Bot using @BotFather telegram bot. Remember to save your telegram token.
Then we have to make our local host public using ngrok. We need to make public our 8080 ,8081 and 1880 port of our local host.
We provide a ``` ngrok.yml ``` that need to be replace in the folder  
```
/home/username/.config/ngrok
```
To install this project use these commands: 
```
$ git clone https://github.com/ghinato97/IoT_Medical_Sport_Examination
$ cd ../path/to/the/file
$ pip3 install -r requirements.txt 
```
After that you need to add the new url  create by ngrok in the Catalog.json located in ```/Catalog``` and the run the others script:

```
$ cd ../Catalog
$ python3 M_Catalog_Rest.py
$ cd ../Device_Connector
$ python3 M_All_Sensor_Call.py
$ python3 All_sensor_MQTT_TS_PUB.py
$ cd ../Database
$ python3 Database.py
$ cd ../BPM
$ python3 M_BPM.py
$ cd ../Controllo_Emergency
$ python3 Controllo_Emergency_Button.py
$ cd ../Telegram_Bot
$ python3 timer.py
$ python3 Mexa_Bot_Telegram.py
```
The folder ```Raspberry ```  must have to be located in the rasperry , in our case we put it in the Desktop 
On your raspberry:
```
$ $ cd Desktop/Rasperry
$ python3 Controllo.py
```

 




