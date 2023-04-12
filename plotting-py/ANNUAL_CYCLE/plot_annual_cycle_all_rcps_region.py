#! /usr/bin/python
# coding: utf-8
import matplotlib.pyplot as plt
import os
import pandas as pd
import glob
import numpy as np
import seaborn as sns
from cmcrameri import cm
from design_matrix_tool import design_df_mean
from colortable import colortable

'''
Contact: Kaharina Buelow

Script for plotting 6x4 annualcycle on one page
Columns are regions, rows are heights 
Input  ../data/*.csv

'''

def create_plot(df,var):
    ''' make line plot '''
    
    colors={'rcp85_1971-2000':cm.lajolla(0.5),
            'rcp85_2021-2050':cm.lajolla(0.7),
            'rcp85_2069-2098':cm.lajolla(0.9),
            'rcp45_1971-2000':cm.lajolla(0.1),
            'rcp45_2021-2050':cm.lajolla(0.3),
            'rcp45_2069-2098':cm.lajolla(0.5),
            'rcp26_1971-2000':cm.roma(0.7),
            'rcp26_2021-2050':cm.roma(0.8),
            'rcp26_2069-2098':cm.roma(1.0)}
    
    plt.figure()
    
    for reg in df['region'].unique():
        #('Alps','Eastern E.','Iberian P.','Scandinavia'):
        sel=df.loc[(df['region'] == reg)]
        # some exceptions:
        if var == 'snowday':
            if reg == 'Scandinavia':
                ymax=31
            elif reg == 'Iberian P.':
                ymax=3.5
            else:
                ymax=23

        if var == 'sca':          
            if reg == 'Scandinavia':
                ymax=100
            elif reg == 'Iberian P.':
                ymax=12
            else:
                ymax=80
                
        print(reg)
        if reg == 'Iberian P.':
            regp = 'IberianPeninsula'
        elif reg == 'Eastern E.':
            regp = 'EasternEurope'
        else:
            regp=reg
        print(regp, ymax)
        
        g=sns.relplot(x='month',
                      y=var,
                      data=sel,
                      err_style="band", 
                      errorbar=('pi',95),
                      estimator='mean',
                      hue='timeslice_rcp',
                      hue_order=['rcp26_1971-2000','rcp26_2021-2050','rcp26_2069-2098',
                                'rcp45_1971-2000','rcp45_2021-2050','rcp45_2069-2098',
                                'rcp85_1971-2000','rcp85_2021-2050','rcp85_2069-2098'],
                      palette=colors,
                      kind='line',
                      col='exp',
                      col_order=['rcp26','rcp45','rcp85'], 
                      row='region')
                      #height=1, aspect=2)
        g.set_xticklabels(['S','O','N','D','J','F','M','A','M','J','J','A'])
        g.set_axis_labels(xname, yname)
        g.set_titles(row_template='{row_name}', col_template='{col_name}')
                        
        g.set(ylim=(ymin, ymax))

        sns.move_legend(g, "center right" ) #, bbox_to_anchor=(.55, .45))
          
        plotname= plotdir+regp+'_'+var+'_annualcycle_all_rcps.png'
        plt.savefig(plotname, bbox_inches="tight")

    return
#
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# Select what you like to plot here:
#
#var_meta_dict = {'snw':[' Snowcover ', 'sca', '%', (0,100)],}
var_meta_dict = {'snw':[' Snowday ', 'snowday', 'number', (0,16)],}


print(os.getcwd())
workdir=os.getcwd()

# better put plots in work:
plotdir=workdir.replace('plotting-py/ANNUAL_CYCLE','plots/ANNUAL_CYCLE')


if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

datadir=workdir.replace('plotting-py/ANNUAL_CYCLE','data')
infile='snw_tas_pr_snowday-snowcover_timeslice_annalcyle_all_level_owd_norm.csv'
input=os.path.join(datadir,infile)
print(' ')
print ('Reading data from = ', input)
print(' ')

#
#--------------------------------------------------
# 
# make plot for each rcp
#
#-------------------------------------------------
#
rcps = ('rcp26', 'rcp45', 'rcp85')

for parameter in var_meta_dict.keys():
    varlongname = var_meta_dict[parameter][0]
    var = var_meta_dict[parameter][1]
    einheit = var_meta_dict[parameter][2]
    ymin = var_meta_dict[parameter][3][0]
    ymax = var_meta_dict[parameter][3][1]

#!!!!!!!!!!!!!!!!!!!!!!!!
dfo = pd.read_csv(input)
#!!!!!!!!!!!!!!!!!!!!!!!!
#
# some adjustments have to be made to data frame,
# because it contails more region, than we like to plot later
#
print(dfo.shape)
df=design_df_mean(dfo)
print('df: ',df.shape)

# sort the dataframe and select what we like to plot

sel1=df[['height','exp','region',var+'_1972-2001','month','RCM','GCM',]]
sel1['timeslice']='1971-2000'
sel1.rename(columns = {var+'_1972-2001':var}, inplace = True)
print('sel1: ',sel1.shape)
sel2=df[['height','exp','region',var+'_2022-2051','month','RCM','GCM',]]
sel2['timeslice']='2021-2050'
sel2.rename(columns = {var+'_2022-2051':var}, inplace = True)
print('sel2: ',sel2.shape)
sel3=df[['height','exp','region',var+'_2070-2099','month','RCM','GCM']]
sel3['timeslice']='2069-2098'
sel3.rename(columns = {var+'_2070-2099':var} , inplace = True)
print('sel3: ',sel3.shape)

df_neu = pd.concat([sel1,sel2,sel3],ignore_index=True, sort=False)

# only added to define the color in the plots
df_neu['timeslice_rcp']=df_neu['exp']+'_'+df_neu['timeslice']

# plotting:

xname = 'month'
yname = varlongname+' ['+einheit +']'
   
sel = df_neu.loc[(df_neu['height'] == 'mean')] 
     
#    sel['varC']=sel[var]-273.15
print('var= ',var)   
print('sel, shape: ',sel.shape, sel['timeslice'].unique())

create_plot(sel,var)
   

