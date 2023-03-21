#! /usr/bin/python
# coding: utf-8
import matplotlib.pyplot as plt
import os
import pandas as pd
from scattertable import scattertable
import glob
import seaborn as sns
from matplotlib import markers
from design_matrix_tool import design_df

'''
Contact: Kaharina Buelow
Script for plotting 6x4 scatterplots on one page
Input  ../data/*.csv

'''
#
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
print(os.getcwd())
workdir=os.getcwd()

datadir=workdir.replace('plotting-py/SCATTER','data')
print(' ')
print('datafile is read from: ', datadir)
        
infile='snw_tas_pr_snowday-snowcover_NA_timeslice_areamean_all_level_owd.csv'
input=os.path.join(datadir,infile)
print(' ')
print ('Reading data from = ', input)
print(' ')

#!!!!!!!!!!!!!!!!!!!!!!!!
dfo = pd.read_csv(input)
#!!!!!!!!!!!!!!!!!!!!!!!!
#
# some adjustments have to be made to data frame
#
df=design_df(dfo)
#!!!!!!!!!!!!!!!!!!!!!!!!!

plotdir=datadir.replace('data','plots/SCATTER/change/')

if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Select what you like to plot here:
#
#var_meta_dict = {'snw':[r'$\Delta$' +' Snow Water Eq.', 'snw', '%', 'pro_diff', (-100,10)],}
#var_meta_dict = {'snw':[r'$\Delta$' +' Snow Day ', 'snowday', '%', 'pro_diff', (-100,5)],}
#var_meta_dict = {'pr':[r'$\Delta$' +' Precipitation ', 'pr', '%', 'pro_diff', (-50,50)],}
var_meta_dict = {'snw':[r'$\Delta$' +' Snowcover ', 'sca', '%', 'diff', (-60,2)],}

var2_meta_dict = {'snw':[r'$\Delta$' +' Snow Day ', 'snowday', 'Number', 'diff', (-35,0)],}
#var2_meta_dict = {'snw':[r'$\Delta$' +' Snow Day ', 'snowday', '%', 'pro_diff', (-100,10)],}
#var2_meta_dict = {'temp':[r'$\Delta$' +' Temperature', 'tas', 'K', 'diff', (0, 7)],}
		       
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# RCP, Timeslice, Regions
rcps = ('rcp26', 'rcp45', 'rcp85')

#year
timeslice = ('2022-2051', '2070-2099')
timeslicep = ('2021-2050', '2069-2098')


#---------------------------------------------------------
# Definition der Variablen mit den Inhalten der Dictionaries
# Variable 1 
for parameter in var_meta_dict.keys():
	varlongname1 = var_meta_dict[parameter][0]
	variable = var_meta_dict[parameter][1]
	einheit1 = var_meta_dict[parameter][2]
	diffmethod = var_meta_dict[parameter][3]
	xmin = var_meta_dict[parameter][4][0]
	xmax = var_meta_dict[parameter][4][1]
	
# Variable 2
for parameter in var2_meta_dict.keys():
	varlongname2 = var2_meta_dict[parameter][0]
	variable2 = var2_meta_dict[parameter][1]
	einheit2 = var2_meta_dict[parameter][2]
	diffmethod2 = var2_meta_dict[parameter][3]
	ymin = var2_meta_dict[parameter][4][0]
	ymax = var2_meta_dict[parameter][4][1]

#--------------------------------------------------
# 
# make plot for each rcp and time slice
#
#-------------------------------------------------    
for rcp in rcps:
    for time in range(len(timeslice)):
        print(timeslice[time])
        			
        colors   = scattertable('colors')
        marker   = scattertable('marker')
        edgecolor="none"
        xname=varlongname1+' ['+einheit1+']'
        yname=varlongname2+' ['+einheit2 +']'

        sel =  df.loc[ (df['exp'] == rcp) ]
        x_column=diffmethod+'_'+variable+'_'+timeslice[time]
        y_column=diffmethod2+'_'+variable2+'_'+timeslice[time]
               
        
        g=sns.relplot(x=x_column, y=y_column,
                      data=sel, kind='scatter',
                      style='GCM',
                      hue='RCM',s=30,
                      palette=colors,
                      alpha=0.8, edgecolor=edgecolor,
                      markers=marker,
                      col='region',
                      col_order=['Alps','Eastern E.','Iberian P.','Scandinavia'],
                      row='height',
                      row_order=['3000','2500','2000','1500','1000','500'],
                      height=2, aspect=1)

        g.map(plt.axhline, y=0, lw=0.5, c='black')
        g.map(plt.axvline, x=0, lw=0.5, c='black')
        
        g.set_axis_labels(xname, yname)
        g.set_titles(row_template='{row_name} [m]', col_template='{col_name}') 
        g.set(xlim=(xmin, xmax))
        g.set(ylim=(ymin, ymax))
        g.fig.suptitle(rcp+': difference '+timeslicep[time]+ ' - 1971-2000')
        #g.fig.subplots_adjust(top=.8)
       
        sns.move_legend(g, "center right" ) #, bbox_to_anchor=(.55, .45))
        
        # delete empty plots
        g.fig.delaxes(g.axes[0, 3]) #SC
        g.fig.delaxes(g.axes[1, 3]) #SC
        g.fig.delaxes(g.axes[0, 1]) #EA
        g.fig.delaxes(g.axes[1, 1]) #EA	
        g.fig.delaxes(g.axes[0, 2]) #IP	
        g.fig.delaxes(g.axes[4, 2]) #IP
        g.fig.delaxes(g.axes[5, 2]) #IP
        
        plotname= plotdir+rcp+'_'+variable+'-'+variable2+'_absolut_scatter_'+timeslice[time]+'_1972-2001.png'
               
        plt.savefig(plotname, bbox_inches="tight")

		

			
	


