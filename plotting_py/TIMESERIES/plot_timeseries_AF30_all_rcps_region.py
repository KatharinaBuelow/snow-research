#! /usr/bin/python
# coding: utf-8
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

    title_fs = 16
    axis_label_fs = 16
    tick_label_fs = 16
    legend_label_fs = 16

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
    
    # seaborn compatibility:
    # - seaborn>=0.12 supports `errorbar=("pi", 50)` percentiles
    # - seaborn<=0.11 does NOT accept `errorbar=` for relplot/lineplot
    #   (it leaks into matplotlib and fails), so we fall back to `ci=50`.
    def _sns_version_tuple(v):
        parts = str(v).split(".")
        out = []
        for p in parts[:3]:
            try:
                out.append(int(p))
            except ValueError:
                break
        return tuple(out)

    supports_errorbar = _sns_version_tuple(sns.__version__) >= (0, 12)

    relplot_kwargs = dict(
        x="year",
        y=var,
        data=df,
        hue="exp",
        hue_order=["rcp26", "rcp45", "rcp85"],
        palette=colrcp,
        kind="line",
        row="region",
        row_order=["Alps", "Eastern E.", "Iberian P.", "Scandinavia"],
        err_style="band",
        estimator=np.median,
        height=2,
        aspect=6,
        facet_kws={"sharey": False, "sharex": True},
    )

    if supports_errorbar:
        g = sns.relplot(
            **relplot_kwargs,
            errorbar=("pi", 90),
        )
    else:
        g = sns.relplot(
            **relplot_kwargs,
            ci=90,
        )

    # Axis labels: by default (1 column) seaborn puts a y label on every row,
    # which can overlap when the facets are tightly stacked. Use a single y label.
    for ax in g.axes.flat:
        ax.set_xlabel("")
        ax.set_ylabel("")

    mid_row = int(g.axes.shape[0] // 2)
    g.axes[mid_row, 0].set_ylabel(yname, fontsize=axis_label_fs, labelpad=15)

    # Push x label lower on the bottom panel
    g.axes[-1, 0].set_xlabel(xname, fontsize=axis_label_fs, labelpad=35)
    g.set_titles(row_template='{row_name}', size=title_fs) #, col_template='{col_name}')
    g.set(xlim=(xmin, xmax))
    g.set(xticks=range (xmin,xmax,10))

    # Tick label sizes on all facets
    for ax in g.axes.flat:
        ax.tick_params(axis="both", which="both", labelsize=tick_label_fs)

    # Keep original autoscaling, but force y-axis to start at 0.
    # If the panel range includes these values, use nice % ticks.
    for ax in g.axes.flat:
        ax.set_ylim(bottom=0)
        ymax_current = ax.get_ylim()[1]
        candidate_ticks = [0, 25, 50, 75, 100]
        ticks_in_range = [t for t in candidate_ticks if t <= ymax_current + 1e-9]
        if 25 in ticks_in_range:
            ax.set_yticks(ticks_in_range)


    # labely on right side of y-axis
    for s, ax in g.axes_dict.items():
        ax1 = ax.twinx()
        ax1.set_yticks(ax.get_yticks())
        ax1.set_ylim(ax.get_ylim())
        ax1.tick_params(axis="y", which="both", labelsize=tick_label_fs)

    # Legend at the bottom
    sns.move_legend(
        g,
        "lower center",
        bbox_to_anchor=(0.5, -0.03),
        ncol=3,
        title=None,
        frameon=False,
    )
    if g.legend is not None:
        for text in g.legend.texts:
            text.set_fontsize(legend_label_fs)
    
    plotname= os.path.join(plotdir, var+'_timeseries_all_rcps_median_pi_90.png')
    plt.savefig(plotname, bbox_inches="tight")
    print("Plot saved: ", plotname)

    return g
#
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# Select what you like to plot here:
#
#var_meta_dict = {'AF30':[' Snowcover (AF30) ', 'AF30_pro', '%', (-100,0),(1986,2084)],}
var_meta_dict = {'AF30':[' SCF30D ', 'AF30', '%', (0,100),(1972,2099)],}

#var_meta_dict = {'snw':[' Snowday ', 'snowday', 'number', (0,16)],}

#infile='DIFF-AF30-year_timeseries_all_level_owd.csv'
infile='AF30-year_timeseries_all_level_owd.csv'
print(os.getcwd())
workdir=os.getcwd()

# plot
plotdir=os.path.join(workdir,'plots','TIMESERIES','AF30')

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
df=design_df_mean(dfo)
#print('df: ',df.shape)

xname = 'year'
yname = varlongname+' ['+einheit +']'
print(' ')
print ('making plot for variable =', var)
print (' ')
create_plot(df,var)
   

