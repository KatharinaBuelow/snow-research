#! /usr/bin/python
# coding: utf-8
import numpy as np
import glob
import matplotlib.pyplot as plt
import subprocess
import os
from matplotlib import markers
import pandas as pd
import seaborn as sns
from snow_plotting_tools import boxplot_all_exp_region

'''
Contact: Katharina Buelow
Script for each region and time slice and high levels sca [%] comparing scenarios
Input  ../data/

'''
# prepare boxplot for snow cover [%]
#var='sca'
# prepare boxplot for snowcoverduration [day]
# Nov-April Numer per month
#var='snowday'
# prepare boxplot with swe [?]
var='snw'

# prepare boxplot for each region
reg = ['AL', 'EU', 'EA', 'IP', 'SC']
title = ['Alps', 'Europe', 'Eastern Europe', 'Iberian Peninsula', 'Scandinavia']

#------------------------------
# directory an In and outfile:
#------------------------------

print(os.getcwd())
workdir=os.getcwd()

datadir=workdir.replace('plotting-py/BOXPLOT','data')
print(' ')
print('datafile is read from: ', datadir)
infile='snw_tas_pr_snowday-snowcover_NA_timeslice_areamean_all_level_owd.csv'
input=os.path.join(datadir,infile)
print(' ')
print ('Reading data from = ', input)
print(' ')

#!!!!!!!!!!!!!!!!!!!!!!!!
df = pd.read_csv(input)
#!!!!!!!!!!!!!!!!!!!!!!!!

# column names of Dateframe:
   # file,season,exp,RCM,region,height,snw_1972-2001,pr_1972-2001,tas_1972-2001
   # snowday_1972-2001,sca_1972-2001,
   # snw_2022-2051,pr_2022-2051,tas_2022-2051,snowday_2022-2051,sca_2022-2051,
   # snw_2070-2099,pr_2070-2099,tas_2070-2099,snowday_2070-2099,sca_2070-2099,
   # GCM,diff_snw_2022-2051,pro_diff_snw_2022-2051,diff_pr_2022-2051,
   # pro_diff_pr_2022-2051,diff_tas_2022-2051,diff_snowday_2022-2051,
   # pro_diff_snowday_2022-2051,diff_sca_2022-2051,
   # diff_snw_2070-2099,pro_diff_snw_2070-2099,diff_pr_2070-2099,
   # pro_diff_pr_2070-2099,diff_tas_2070-2099,diff_snowday_2070-2099
   # pro_diff_snowday_2070-2099,diff_sca_2070-2099

plotdir=datadir.replace('data','plots/BOXPLOTS/single_timeslice_region/')
# better move to work


if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

#---------------------------------------------
# prepare dataframe:
#--------------------------------------------

df['height'].replace('0','500', inplace=True)
df['height'].replace('1','1000', inplace=True)
df['height'].replace('2','1500', inplace=True)
df['height'].replace('3','2000', inplace=True)
df['height'].replace('4','2500', inplace=True)
df['height'].replace('5','3000', inplace=True)

df['exp_n']=df['exp']

# 1. Plots for each region/timeslice, comparisons of the hue=experiment 

sel1=df[['height','exp','region',var+'_1972-2001']]
print('vorher: ',sel1.columns.unique())
sel1.loc[:,'timeslice'] = '1971-2000'

sel1.rename(columns = {var+'_1972-2001':var}, inplace = True)

#a) select historical rcp85
# rename exp-column with rcp85 to rcp85-1971-2000
sela=sel1.loc[(sel1['exp'] == 'rcp85')]

sela['experiment'] = sela['exp'].str.cat(sela['timeslice'],sep="-")
selb=sela.drop(columns=['exp'])

sel2=df[['height','exp','region',var+'_2022-2051']]
sel2['timeslice']='2021-2050'
sel2.rename(columns = {var+'_2022-2051':var}, inplace = True)

sel3=df[['height','exp','region',var+'_2070-2099']]
sel3['timeslice']='2069-2098'
sel3.rename(columns = {var+'_2070-2099':var}, inplace = True)

df_neu = pd.concat([sel1,sel2,sel3],ignore_index=True)

# just to make it look nicer on the plot
df_neu.rename(columns = {'exp':'experiment'}, inplace = True)

print(df_neu.columns.unique())
print(sel1.shape)
print(selb.shape)
print(sel2.shape)
print(sel3.shape)
print(df_neu.shape)

print(selb.columns.unique())

time=('2021-2050', '2069-2098')
for t in time:
    selc= df_neu.loc[ (df_neu['timeslice'] == t)]
    sel = pd.concat([selc,selb], ignore_index=True)
    print('hier')
    for r in range(len(reg)):
        print('prepare plot for: ', reg[r] )
        print('title: ', title[r]+' '+ t)
        sel1r = sel.loc[ (sel['region'] == reg[r])]
        print(sel1r.shape)
        print(sel1r)
        sel1r.reset_index(drop=True)
        plottitle='November-April '+t+' '+title[r]
        boxplot_all_exp_region(sel1r, plotdir, plottitle, reg[r],t, var)

