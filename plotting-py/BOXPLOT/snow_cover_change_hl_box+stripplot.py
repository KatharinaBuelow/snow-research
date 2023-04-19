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
from snow_plotting_tools import boxplot_single_exp_region

'''
Contact: Katharina Buelow
Script for each region and each scenarios and high levels sca [%]
Input  ../data/

'''
# prepare boxplot for snow cover [%]
var='sca'

# prepare boxplot for snowcoverduration [day]
# Nov-April Numer per month
var='snowday'

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

plotdir=datadir.replace('data','plots/BOXPLOTS/single_exp_region/')
#better move to work

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


# 1. Plots for each region/experiment, comparisons of the hue=timeslice 

sel1=df[['height','exp','region',var+'_1972-2001']]
sel1['timeslice']='1971-2000'
sel1.rename(columns = {var+'_1972-2001':var}, inplace = True)

sel2=df[['height','exp','region',var+'_2022-2051']]
sel2['timeslice']='2021-2050'
sel2.rename(columns = {var+'_2022-2051':var}, inplace = True)

sel3=df[['height','exp','region',var+'_2070-2099']]
sel3['timeslice']='2069-2098'
sel3.rename(columns = {var+'_2070-2099':var}, inplace = True)

df_neu = pd.concat([sel1,sel2,sel3])

for e in df_neu['exp'].unique():
    sel= df_neu.loc[ (df_neu['exp'] == e)]
    for r in range(len(reg)):
        print('prepare plot for: ', reg[r] )
        print('title: ', title[r]+' '+ e )
        sel1r = sel.loc[ (sel['region'] == reg[r])]
        print(sel1r.shape)
        plottitle='November-April '+title[r]+' '+ e
        boxplot_single_exp_region(sel1r, plotdir, plottitle, reg[r], e, var)

