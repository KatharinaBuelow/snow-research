#! /usr/bin/python
# coding: utf-8
import matplotlib.pyplot as plt
import os
import pandas as pd
import glob
import numpy as np
import seaborn as sns
from cmcrameri import cm
from design_matrix_tool import design_df
from colortable import colortable

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

    colrcp= {'rcp85':cm.lajolla(0.7),
             'rcp45':cm.lajolla(0.3),
             'rcp26':cm.roma(0.8)}
    

    #fig =
    plt.figure() #figsize=(20, 15))

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
        col='region',
        col_order=['Alps', 'Eastern E.','Iberian P.', 'Scandinavia'],
        row='height',
        row_order=['3000','2500','2000','1500','1000','500'],
        #errorbar=(lambda x: (x.min(), x.max())),
        err_style="band", 
        errorbar=('pi',95),
        #ci='sd',
        #estimator="median", 
        estimator='mean',
        height=2, #2,
        aspect=4, #6,
        facet_kws={'sharey': True, 'sharex': True}
    )
    
    g.set_axis_labels(xname, yname)
    g.set_titles(row_template='{row_name}', col_template='{col_name}')
    g.set(xlim=(xmin, xmax))
    g.set(xticks=range(xmin,xmax,10))
    g.set(ylim=(ymin, ymax))
    g.set(yticks=range(ymin,ymax,dy))

    # delete empty plots
    g.fig.delaxes(g.axes[0, 3]) #SC
    g.fig.delaxes(g.axes[1, 3]) #SC
    g.fig.delaxes(g.axes[0, 1]) #EA
    g.fig.delaxes(g.axes[1, 1]) #EA
    g.fig.delaxes(g.axes[0, 2]) #IP
    g.fig.delaxes(g.axes[4, 2]) #IP
    g.fig.delaxes(g.axes[5, 2]) #IP
    
    # labely on right side of y-axis
    #for s, ax in g.axes_dict.items():
    #    ax1 = ax.twinx()
    #    ax1.set_yticks(ax.get_yticks())
    #    ax1.set_ylim(ax.get_ylim())

    # Legend at the bottom
    sns.move_legend(g, "lower center" , bbox_to_anchor=(.5, -0.03), ncol=3, title=None, frameon=False,)

   
    plotname= os.path.join(plotdir, var+'_timeseries_all_rcps_heights_regions_mean_pi_95.png')
    plt.savefig(plotname, bbox_inches="tight")
    print("Plot saved: ", plotname)

    return
#
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# Select what you like to plot here:

# var_meta_dict = {'Temperature':[r'$\Delta$ Temperature ', 'tas_diff', 'K', (0,5),(1986,2084),1],}
#var_meta_dict = {'Precipitation':[r'$\Delta$ Precipitation ', 'pr_pro', '%', (-30,30),(1986,2084),10],}
var_meta_dict = {'Snowcover':[r'$\Delta$ Snowcover ', 'sca_pro', '%', (-100,30),(1986,2084),20],}
#var_meta_dict = {'Snowday':[' Snowday ', 'sd_pro', '%', (-100,0),(1986,2084),10],}
#var_meta_dict = {'snw':[' Snow water eq.', 'snw_pro', '%', (-100,10),(1986,2084),10],}

var_name='sca'
infile='DIFF-'+var_name+'-year_timeseries_all_level_owd.csv'
print(infile)

print(os.getcwd())
workdir=os.getcwd()

# better put plots in work:
plotdir='/work/ch0636/g300047/SNOW-RESEARCH/plots/TIMESERIES/'+var_name

if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

datadir=workdir.replace('plotting-py/TIMESERIES','data')
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
df=design_df(dfo)
print('df: ',df.shape)
print(var,' : ',df[var])
xname = 'year'
yname = varlongname+' ['+einheit +']'
print(' ')
print ('making plot for variable =', var)
print (' ')
create_plot(df,var)
   

