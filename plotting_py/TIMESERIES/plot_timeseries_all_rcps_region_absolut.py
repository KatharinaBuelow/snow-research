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
from plotting_py.TIMESERIES.design_matrix_tool import design_df_mean
from plotting_py.TIMESERIES.colortable import colortable

print('seabornversion: ')
print(sns.__version__)
# required 0.12.0, Use the new `errorbar` parameter for more flexibility.

'''
Contact: Kaharina Buelow

Script for plotting 4 timeseries on top of each other on one page
rows are regions 
Input  ../data/*.csv

'''

def create_plot(df,var):
    ''' make line plot '''

    colrcp= {'rcp45':cm.lajolla(0.7),
             'rcp85':cm.lajolla(0.3),
             'rcp26':cm.roma(0.8)}
    

    fig = plt.figure(figsize=(20, 15))

    # Errorbars:
    #https://seaborn.pydata.org/tutorial/error_bars.html?highlight=min+max+percentile
    # if nothing is set ci= int (bootstrapping), which calculates 95% confidence intervall with bootstrapping and draws the mean
    # mean can be changes estimator=median
    #
    # errorbar=("se", 2)
    # errorbar="pi" will show a 95% interval is nothing is set, ranging from the 2.5 to the 97.5 percentiles.
    # errorbar =('pi',50) e.g., to show the inter-quartile range
    # errorbar =('pi',100) show all; same like: (lambda x: (x.min(), x.max()))
    
    g=sns.relplot(
        x='year',
        y=var,
        data=df,
        hue='exp',
        hue_order=['rcp26','rcp45','rcp85'],
        palette=colrcp,
        kind='line',
        row='region',
        row_order=['Alps', 'Eastern E.','Iberian P.', 'Scandinavia'], 
        #errorbar=(lambda x: (x.min(), x.max())),
        err_style="band", 
        errorbar=('pi',50),
        #ci='sd',
        estimator="median", 
        #estimator='mean',
        height=2,
        aspect=6,
        facet_kws={'sharey': False, 'sharex': True}
    )
    
    g.set_axis_labels(xname, yname)
    g.set_titles(row_template='{row_name}') #, col_template='{col_name}')
    g.set(xlim=(xmin, xmax))
    g.set(xticks=range(xmin,xmax,10))
    #g.set(ylim=(ymin, ymax))
    #g.set(yticks=range(ymin,ymax,dy))
    
    
    # labely on right side of y-axis
    for s, ax in g.axes_dict.items():
        ax1 = ax.twinx()
        ax1.set_yticks(ax.get_yticks())
        ax1.set_ylim(ax.get_ylim())
        if einheit == '%':
            ax1.axhline(0, ls='--', c='grey')
        
    # Legend at the bottom
    sns.move_legend(g, "lower center" , bbox_to_anchor=(.5, -0.03), ncol=3, title=None, frameon=False,)
    
    plotname= os.path.join(plotdir, var+'_timeseries_all_rcps_median_pi_50.png')
    plt.savefig(plotname, bbox_inches="tight")
    print("Plot saved: ", plotname)

    return g
#
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# Select what you like to plot here:

#var='snowcover'
var='snw'
infile=var+'-year_timeseries_all_level_owd.csv'
#var_meta_dict = {'Temperature':[' Temperature ', 'tas_diff', 'K', (0,6),(1986,2084),1],}
#var_meta_dict = {'Precipitation':[' Precipitation ', 'pr_pro', '%', (-30,30),(1986,2084),10],}
#var_meta_dict = {'Snowcover':['Snow cover fraction', 'snowcover', '%', (0,100),(1972,2099),10],}
#var_meta_dict = {'Snowday':[' Snow day ', 'snowday', 'Number', (0,200),(1972,2099),50],}
var_meta_dict = {'swe':[' Snow water eq. ', 'snw', 'mm', (-100,10),(1972,2099),10],}

print(infile)

print(os.getcwd())
workdir=os.getcwd()

# plotdir
plotdir=os.path.join(workdir,'plots','TIMESERIES',var)

if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

datadir=workdir.replace('plotting_py/TIMESERIES','data')
input=os.path.join(datadir,infile)
print(' ')
print ('Reading data from = ', input)
print(' ')

#
#--------------------------------------------------
# 
# make plot
#
#-------------------------------------------------
#

for parameter in var_meta_dict.keys():
    varlongname = var_meta_dict[parameter][0]
    var = var_meta_dict[parameter][1]
    einheit = var_meta_dict[parameter][2]
    ymin = var_meta_dict[parameter][3][0]
    ymax = var_meta_dict[parameter][3][1]
    dy = var_meta_dict[parameter][5]
    xmin = var_meta_dict[parameter][4][0]
    xmax = var_meta_dict[parameter][4][1]

#!!!!!!!!!!!!!!!!!!!!!!!!
dfo = pd.read_csv(input)
#!!!!!!!!!!!!!!!!!!!!!!!!
#
# some adjustments have to be made to data frame,
# because it contails more region, than we like to plot later
#
print(dfo.shape)
print(dfo['height'].unique())
df=design_df_mean(dfo)
print(df.shape)

xname = 'year'
yname = varlongname+' ['+einheit +']'
print(' ')
print ('making plot for variable =', var)
print (' ')

print ('making plot for exp =', df['exp'].unique())
print ('making plot for exp =', df[var].unique())
create_plot(df,var)
   

