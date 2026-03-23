#! /usr/bin/python
# coding: utf-8
from __future__ import annotations
import sys
from pathlib import Path


# Allow running this script from any working directory by ensuring the repo
# root (the parent of `plotting_py/`) is on sys.path.
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
from plotting_py.TIMESERIES.colortable import colortable
from plotting_py.TIMESERIES.design_matrix_tool import design_df_mean
#from matplotlib.transforms import ScaledTranslation


'''
Contact: Kaharina Buelow

Script for plotting 4x4 annualcycle on one page
Columns are rcps, rows are regions 
Input  ../data/*.csv

'''


def create_plot(df, var, xname, yname, ymin, ymax, plotdir):
    ''' make line plot '''
    
    colors={'rcp45_1971-2000':cm.lajolla(0.9),
            'rcp45_2021-2050':cm.lajolla(0.7),
            'rcp45_2069-2098':cm.lajolla(0.5),
            'rcp85_1971-2000':cm.lajolla(0.5),
            'rcp85_2021-2050':cm.lajolla(0.3),
            'rcp85_2069-2098':cm.lajolla(0.1),
            'rcp26_1971-2000':cm.roma(0.7),
            'rcp26_2021-2050':cm.roma(0.8),
            'rcp26_2069-2098':cm.roma(1.0)}
    
    #plt.figure()
    
    g=sns.relplot(x='month',
                  y=var,
                  data=df,
                  err_style="band", 
                  errorbar=('pi',95),
                  estimator='median',
                  hue='rcp_timeslice',
                  hue_order=['rcp26_1971-2000','rcp26_2021-2050','rcp26_2069-2098',
                             'rcp45_1971-2000','rcp45_2021-2050','rcp45_2069-2098',
                             'rcp85_1971-2000','rcp85_2021-2050','rcp85_2069-2098'],
                  palette=colors,
                  kind='line',
                  col='exp',
                  col_order=['rcp26','rcp45','rcp85'], 
                  row='region',
                  row_order=['Alps','Eastern E.','Iberian P.','Scandinavia'],
                  height=2, aspect=1.5,
                  facet_kws={'sharey': False, 'sharex': True})
    g.set_xticklabels(['S','O','N','D','J','F','M','A','M','J','J','A'])
    g.set_axis_labels(xname, yname)
    g.set_titles(row_template='{row_name}', col_template='{col_name}')

    # Align y-labels after seaborn has positioned everything.
    #g.fig.canvas.draw()
    #align_ylabel_vertically(g)

    # Set different ymax for each region (apply to every column in that row)
    region_order = ['Alps', 'Eastern E.', 'Iberian P.', 'Scandinavia']
    axes = np.asarray(g.axes)
    if axes.ndim == 1:
        axes = axes.reshape(-1, 1)
    for row_idx, region in enumerate(region_order):
        if var =='snw':
            if region == 'Scandinavia':
                region_ymax = 200
            elif region == 'Iberian P.':
                region_ymax = 25
            elif region == 'Eastern E.':
                region_ymax = 50
            else:  # Alps or any other
                region_ymax = ymax
        elif var == 'snowday':
            if region == 'Scandinavia':
                region_ymax = 31
            elif region == 'Iberian P.':
                region_ymax = 4
            else:   
                region_ymax = ymax
        elif var == 'sca':
            if region == 'Scandinavia':
                region_ymax = 100
            elif region == 'Iberian P.':
                region_ymax = 12
            else:   
                region_ymax = ymax
                
        for ax in axes[row_idx, :]:
            ax.set_ylim(ymin, region_ymax)
    #g.set(ylim=(ymin, ymax))

    sns.move_legend(g,'lower center', scatterpoints = 1, bbox_to_anchor=(0.45, -0.1),fancybox=True, shadow=True, ncol=3 )

    plotname = os.path.join(plotdir, f"all_regions_{var}_median_annualcycle_all_rcps.png")
    plt.savefig(plotname, bbox_inches="tight")

    return

#
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# Select what you like to plot here:
#
#var_meta_dict = {'snw':[' Snow cover fraction ', 'sca', '%', (0,80)],}
#var_meta_dict = {'snw':[' Snow day ', 'snowday', 'number', (0,25)],}
var_meta_dict = {'snw':[' Snow water eq. ', 'snw', 'mm', (0,250)],}

print(os.getcwd())
workdir=os.getcwd()

# Put outputs relative to the repo root, independent of the current working dir.
_plots_root = _REPO_ROOT / ('PLOTS' if (_REPO_ROOT / 'PLOTS').is_dir() else 'plots')
plotdir = str(_plots_root / 'ANNUAL_CYCLE')

if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

datadir = str(_REPO_ROOT / 'data')
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
df=design_df_mean(dfo)
print('df: ',df.shape)

# sort the dataframe and select what we like to plot

sel1 = df[['height','exp','region',var+'_1972-2001','month','RCM','GCM',]].copy()
sel1['timeslice'] = '1971-2000'
sel1 = sel1.rename(columns={var+'_1972-2001': var})
print('sel1: ', sel1.shape)
sel2 = df[['height','exp','region',var+'_2022-2051','month','RCM','GCM',]].copy()
sel2['timeslice'] = '2021-2050'
sel2 = sel2.rename(columns={var+'_2022-2051': var})
print('sel2: ', sel2.shape)
sel3 = df[['height','exp','region',var+'_2070-2099','month','RCM','GCM']].copy()
sel3['timeslice'] = '2069-2098'
sel3 = sel3.rename(columns={var+'_2070-2099': var})
print('sel3: ', sel3.shape)

df_neu = pd.concat([sel1,sel2,sel3],ignore_index=True, sort=False)

# only added to define the color in the plots
df_neu['rcp_timeslice']=df_neu['exp']+'_'+df_neu['timeslice']

# plotting:

xname = 'month'
yname = varlongname+' ['+einheit +']'
   
sel = df_neu.loc[(df_neu['height'] == 'mean')] 
     
#    sel['varC']=sel[var]-273.15
print('var= ',var)   
print('sel, shape: ',sel.shape, sel['timeslice'].unique())

create_plot(sel, var, xname, yname, ymin, ymax, plotdir)
   

