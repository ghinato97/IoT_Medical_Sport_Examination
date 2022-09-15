# Table of Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Set- up](#set-up)


## General Info
This is a repository for a IoT project of Politecnico of Turin.
The proposed IoT platform aims at monitoring vital signs of the patient under stress condition during a sports medical examination in remote mode. 
It integrates different IoT devices that provides us patient’s data such as:
- Pulse Rate
- Respiration Rate
- Saturation
- Perfusion
- Rpm
- Also the patient can switch an emergency button if an emergency occurs

Three leds are employed to guarantee a communication between the doctor and the patient. 
The big red led is used to warn the patient that the session has started by switching it on, the opposite happen for session end.  Two small leds, green and red, are employed to communicate to the patient that his acceleration has to be increased, with the green led blinking, or reduced, with the red blinking. 
The doctor can access real time monitoring of the sensors using the Telegram Bot which provides a link for the 
node-red dashboard. At the end of the session he can choose to see the data plotting of the sensors for the entire session. All data sensors are stored during the session using Thingspeak. Multiple sessions cannot run simultaneously. 

## Technologies
The project is created using:
- rasperry Pi 2
- python 3
- node-red
- thingspeak
- telegram



## Set-up
At first yoy



