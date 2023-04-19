#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from cmcrameri import cm
from matplotlib import markers


def boxplot_single_exp_region(sel1r, plotdir, title,region, e, var):

    print(title)
    OutFile=os.path.join(plotdir,'Boxplot_'+var+'_'+region+'_'+e+'.png')

    #---------------
    # colors
    #--------------
    
    if e == 'rcp85':
        mycol=cm.roma(0.00)
    if e == 'rcp45':
        mycol=cm.roma(0.30)
    if e == 'rcp26':
        mycol=cm.roma(1.00)
              
    fig = plt.figure(figsize=(10,10))
    
    yorder=['3000', '2500','2000','1500','1000','500' ]
    hueorder=['2069-2098','2021-2050','1971-2000']
       
    #sns.stripplot(x=var, y='height', data=sel1r, dodge=True, color='black', alpha=0.7, jitter=0.2, size=4, order=yorder, hue_order= hueorder,hue= 'timeslice')

    #sns.boxplot(x=var, y='height', data=sel1r, whis=np.inf ,order=yorder, hue_order= hueorder,hue= 'timeslice', color=mycol, boxprops=dict(alpha=0.8))

    sns.stripplot(x=var, y='height', data=sel1r, dodge=True, alpha=0.7, jitter=0.2, size=4, order=yorder, color=mycol, split=True, linewidth=1, edgecolor='gray', hue_order= hueorder,hue='timeslice')

    ax=sns.boxplot(x=var, y='height', data=sel1r, whis=np.inf ,order=yorder, hue_order= hueorder,hue='timeslice', color=mycol, boxprops=dict(alpha=0.7))
    
    
    plt.tick_params(bottom=False)
    plt.grid(True)
    #plt.xlim(0,100)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=12)
    if var == 'sca':
        plt.xlim(0,100)
        plt.xlabel('snow cover fraction [%]', fontsize=14)
    if var == 'snowday':
        plt.xlim(0,32)
        plt.xlabel('snow days [days/month]', fontsize=14)
    plt.ylabel('height [m]', fontsize=14)
    plt.title(title, color='k', fontsize=14)
    
    handles, labels = ax.get_legend_handles_labels()
    l = plt.legend(handles[0:3], labels[0:3], loc=2, borderaxespad=0.5)
    
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches='tight')    

    return



def boxplot_all_exp_region(sel1r, plotdir, title,region, t, var):
    ### colors : https://www.fabiocrameri.ch/colourmaps/
    #my_cols = {'rcp85': cm.lajolla(0.7),
    #           'rcp45': cm.lajolla(0.3),
    #           'rcp26': cm.roma(0.8),
    #           'rcp85-1971-2000': cm.lajolla(0.5)}

    my_cols= {'rcp85':cm.lajolla(0.7),
             'rcp45':cm.lajolla(0.3),
             'rcp26':cm.roma(0.8),
             'rcp85-1971-2000': cm.grayC(0.3)}
    
    #my_cols = {'rcp85': cm.roma(0.00),
    #           'rcp45': cm.roma(0.30),
    #           'rcp26': cm.roma(1.00),
    #           'rcp85-1971-2000': cm.roma(0.10)}
    #0.1: braun, 0.3 beige, 1: blau, 0:rotbraun           

    print(title)
    OutFile=os.path.join(plotdir,'Boxplot_'+var+'_'+region+'_'+t+'.png')

    fig = plt.figure(figsize=(10,10))
    
    yorder=['3000', '2500','2000','1500','1000','500' ]
    hueorder=['rcp85','rcp45','rcp26','rcp85-1971-2000' ]
    
    print (' ')
    print (' ')

    print(sel1r)
    sel1r.to_csv('test') 
    print('var = ', var)

    
    sns.stripplot(x=var, y='height', data=sel1r, dodge=True, alpha=0.9, jitter=0.2, size=4, order=yorder, palette=my_cols, linewidth=1, edgecolor='gray', hue_order= hueorder,hue='experiment')
    
    ax=sns.boxplot(x=var, y='height', data=sel1r, whis=np.inf ,order=yorder, hue_order= hueorder,hue='experiment', palette=my_cols, boxprops=dict(alpha=0.8))
    
    plt.tick_params(bottom=False)
    plt.grid(True)
    #plt.xlim(0,100)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=12)
    if var == 'sca':
        plt.xlim(0,100)
        plt.xlabel('snow cover fraction [%]', fontsize=14)
    if var == 'snw':
        plt.xlim(0,1000)
        plt.xlabel('snow water equivalent [mm/day]', fontsize=14)
    if var == 'snowday':
        plt.xlim(0,32)
        plt.xlabel('snow days [days/month]', fontsize=14)
    plt.ylabel('height [m]', fontsize=14)
    plt.title(title, color='k', fontsize=14) 

    handles, labels = ax.get_legend_handles_labels()
    l = plt.legend(handles[0:4], labels[0:4], loc=2, borderaxespad=0.5)  #bbox_to_anchor=(1.05, 1)
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches='tight')    
    
    return
