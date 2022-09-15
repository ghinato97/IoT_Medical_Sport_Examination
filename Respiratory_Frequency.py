import json
from scipy.signal import  find_peaks
import numpy as np

class Resp_Freq():
    def __init__(self,array):
        self.array=array
    def BPM(self):
        picchi=find_peaks(self.array)[0]        
        time_diff=np.diff(picchi)
        time_diff=time_diff.mean()*0.5
        #moltiplichiamo per 0.5 perchè i sensori pubblicano ogni 0.5 secondi
        BPM= int(60/time_diff)
        return BPM
