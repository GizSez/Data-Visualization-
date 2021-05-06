# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 12:30:08 2021

@author: gizig
__author__ = "Gizem Gross" 

__copyright__ = "Copyright 2021, Zürich" 

__credits__ = {"Gizem Gross", "Christian Fischer", "Rolf Böller"}        

__license__ = "TOS" 

__version__ = "2.0.2" 

__maintainer__ = "Uhura" 

__email__ = "grossgiz@students.zhaw.ch" 

__status__ = "not worth mentioning" 

"""

import pollution_processor_301
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import datetime




class Visualization:
    def __init__(self):
        self.processor = pollution_processor_301.Filter_Processor()
        self.mean = self.processor.get_mean()
        self.max = self.processor.get_max()
        self.min = self.processor.get_min()
        self.skewness = self.processor.get_skewness()
        self.kurtosis = self.processor.get_kurtosis()
        self.data = self.processor.get_filtered_data()

    def pollutionDistribution(self):
        self.updatedata()
        min_data = self.min
        max_data = self.max
        mean_data = self.mean
        bins = np.linspace(min_data, max_data, 100)
        mu, std = norm.fit(self.data["Wert"])
        p = norm.pdf(bins, mu, std)
        weights = np.ones_like(bins)/ sum(self.data["Wert"])
        pollution_label = "Pollution Distribution"
        fig, (ax2) = plt.subplots(1, 1, figsize=(16,9))  #Grösse des Plots 
        ax2.hist(self.data["Wert"], density=True, bins=bins,alpha=0.5,label=pollution_label)#Histogramm erzeugen 
        ax2.legend(loc='upper right') #Legendenposition
        textstr = '\n'.join((         #Legendentext
                    r'%s' % ("Pollution",),
                    # t'abs_metric=%.2f' % abs_metric
                    r'$Skewness=%.2f$' % (self.skewness,),
                    r'$Kurtosis=%.2f$' % (self.kurtosis,),
                    r'$Max=%.2f$' % (self.max,),
                    r'$Min=%.2f$' % (self.min,)))
        ax2.set_xlabel('NO2 (µg/m3 )')  #Beschriftungen 
        ax2.set_ylabel('Relative Frequency')
        ax2.set_title('Current Pollution NO2 Molecule Zürich Heubeeribüel')
        props = dict(boxstyle='round', facecolor='red', alpha=0.5)  #Layout Box oben rechts 
        ax2.text(2.5, 0.8, textstr,fontsize=14,verticalalignment='top',bbox=props) #Texpositionierung, layout
        plt.plot(bins, p, "k", linewidth = 2, color = "red") #parametrierung für verteilung der gesamten pollution
        mydate = str(datetime.date.today()) #Hinzugabe eines Datums beim Abspeichern 
        filename = "distribution_"+mydate+".jpg" #Abspeicherung JPG-File im Arbeitsverzeichnis 
        plt.savefig(filename)
        return plt

    def pollutiontime(self):
        self.updatedata()
        fig, (ax) = plt.subplots(1, 1, figsize=(16,9))
        ax.plot(self.data["Datum"], self.data["Wert"], color='tab:orange', label='Pollution')
        ax.set_xlabel('Datum')
        ax.set_ylabel('NO2 (µg/m3 )')
        ax.set_title('Over time Pollution NO2 Molecule Zürich Heubeeribüel')
        ax.grid(True)
        ax.legend(loc='upper left')
        mydate = str(datetime.date.today())
        filename = "ts_"+mydate+".jpg" #Abspeicherung JPG-File im Arbeitsverzeichnis 
        plt.savefig(filename)
        return plt

    def updatedata(self):
        self.data = self.processor.get_filtered_data()
        self.mean = self.processor.get_mean()
        self.max = self.processor.get_max()
        self.min = self.processor.get_min()
        self.skewness = self.processor.get_skewness()
        self.kurtosis = self.processor.get_kurtosis()
        
#Test
if __name__ == "__main__":
    mypollution = Visualization()
    myplot = mypollution.pollutionDistribution()
    myplot2 = mypollution.pollutiontime()
    myplot.show()
    myplot2.show()