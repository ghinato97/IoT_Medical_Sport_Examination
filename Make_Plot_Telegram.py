import pandas as pd
import matplotlib.pyplot as plt
import time

class Make_Plot():
    def __init__(self,path):
        path_csv=path+'/all_data.csv'
        data_frame=pd.read_csv(path_csv)
        time_=data_frame['created_at']
        
        
        accelerometro=data_frame['field1']
        accelerometro=accelerometro.dropna()  
        plt.figure(0)
        accelerometro_plot=accelerometro.plot()
        fig=accelerometro_plot.get_figure()
        fig.savefig(path+'/accelerometer.png')
        
        
        battito=data_frame['field2']
        battito=battito.dropna()
        plt.figure(1)
        battito_plot=battito.plot()
        fig1=battito_plot.get_figure()
        fig1.savefig(path+'/heart_rate.png')
        

        
        saturazione=data_frame['field3']
        saturazione=saturazione.dropna()
        plt.figure(2)
        saturazione_plot=saturazione.plot()
        fig2=saturazione_plot.get_figure()
        fig2.savefig(path+'/saturation.png')
        
               

        
        perfusione=data_frame['field4']
        perfusione=perfusione.dropna()
        plt.figure(3)
        perfusione_plot=perfusione.plot()
        fig3=perfusione_plot.get_figure()
        fig3.savefig(path+'/perfusion.png')
                             
                              