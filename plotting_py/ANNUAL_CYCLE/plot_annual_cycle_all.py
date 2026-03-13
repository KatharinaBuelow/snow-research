#! /usr/bin/python
# coding: utf-8
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import matplotlib.pyplot as plt
import os
import pandas as pd
import glob
import numpy as np
import seaborn as sns
from cmcrameri import cm
from plotting_py.TIMESERIES.design_matrix_tool import design_df

'''
Contact: Kaharina Buelow

Script for plotting 6x4 annualcycle on one page
Columns are regions, rows are heights 
Input  ../data/*.csv

'''

def create_plot(df,var,rcp):
    ''' make line plot '''
    
    plt.figure()

    if rcp == 'rcp85':
        palette=[cm.lajolla(0.5),cm.lajolla(0.7),cm.lajolla(0.9)]
    if rcp == 'rcp45':
        palette=[cm.lajolla(0.1),cm.lajolla(0.3),cm.lajolla(0.5)]
    if rcp == 'rcp26':
        palette=[cm.roma(0.70),cm.roma(0.8),cm.roma(1.0)]

    g=sns.relplot(x='month',
                  y=var,
                  data=df,
                  err_style="band", 
                  errorbar=('pi',95),
                  estimator='mean',
                  hue='timeslice',palette=palette,kind='line',
                  col='region',
                  col_order=['Alps','Eastern E.','Iberian P.','Scandinavia'],
                  row='height',
                  row_order=['3000','2500','2000','1500','1000','500'],
                  height=2, aspect=1)
    g.set_xticklabels(['S','O','N','D','J','F','M','A','M','J','J','A'])
    g.set_axis_labels(xname, yname)
    g.set_titles(row_template='{row_name} [m]', col_template='{col_name}') 
    g.set(ylim=(ymin, ymax))

    sns.move_legend(g, "upper right" , bbox_to_anchor=(0.85, 0.95), ncol=1, title=None, frameon=False,)

    #sns.move_legend(g, "center right" ) #, bbox_to_anchor=(.55, .45))
    # delete empty plots
    g.fig.delaxes(g.axes[0, 3]) #SC
    g.fig.delaxes(g.axes[1, 3]) #SC
    g.fig.delaxes(g.axes[0, 1]) #EA
    g.fig.delaxes(g.axes[1, 1]) #EA
    g.fig.delaxes(g.axes[0, 2]) #IP
    g.fig.delaxes(g.axes[4, 2]) #IP
    g.fig.delaxes(g.axes[5, 2]) #IP

            
    plotname= plotdir+rcp+'_'+var+'_annualcycle_all.png'
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
var_meta_dict = {'snw':[' snow day ', 'snowday', 'number', (0,31)],}

print(os.getcwd())
workdir=os.getcwd()

# better put plots in work:
plotdir=workdir.replace('plotting_py/ANNUAL_CYCLE','plots/ANNUAL_CYCLE')

if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

datadir=workdir.replace('plotting_py/ANNUAL_CYCLE','data')
infile='snw_tas_pr_snowday-snowcover_timeslice_annualcyle_all_level_owd_norm2.csv'
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
df=design_df(dfo)
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

print(df_neu)

# plotting:

xname = 'month'
yname = varlongname+' ['+einheit +']'

# nur zum gucken
#out_file=os.path.join(plotdir,'df_neu.csv')
#df_neu.to_csv(out_file, na_rep='NaN' )

for rcp in rcps:
    
    sel = df_neu.loc[(df_neu['exp'] == rcp)] 
     
    #    sel['varC']=sel[var]-273.15
    print('var= ',var)   
    print('sel, shape: ',sel.shape, rcp, sel['timeslice'].unique())
    
    create_plot(sel,var,rcp)
   

