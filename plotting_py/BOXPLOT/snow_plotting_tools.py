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
    plt.tick_params(axis='y', labelsize=16)
    plt.tick_params(axis='x', labelsize=16)
    if var == 'sca':
        plt.xlim(0,100)
        plt.xlabel('snow cover fraction [%]', fontsize=18)
    if var == 'snowday':
        plt.xlim(0,32)
        plt.xlabel('snow days [days/month]', fontsize=18)
    plt.ylabel('height [m]', fontsize=18)
    plt.title(title, color='k', fontsize=18)
    
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

    #my_cols= {'rcp85':cm.lajolla(0.7),
    #         'rcp45':cm.lajolla(0.3),
    #         'rcp26':cm.roma(0.8),
    #         'rcp85-1971-2000': cm.grayC(0.1)}
    
    my_cols = {'rcp85': cm.roma(0.00),
               'rcp45': cm.lajolla(0.7), #cm.roma(0.30),
               'rcp26': cm.roma(1.00),
               'rcp85-1971-2000': cm.grayC(0.8)}
    # 0.3 beige, 1: blau, 0:rotbraun           

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
    
    sns.stripplot(
        x=var,
        y='height',
        data=sel1r,
        dodge=True,
        alpha=0.9,
        jitter=0.2,
        size=4,
        order=yorder,
        palette=my_cols,
        linewidth=0.4,
        edgecolor='gray',
        hue_order=hueorder,
        hue='experiment',
    )
    
    ax = sns.boxplot(
        x=var,
        y='height',
        data=sel1r,
        whis=np.inf,
        order=yorder,
        hue_order=hueorder,
        hue='experiment',
        palette=my_cols,
        linewidth=0.6,
        boxprops=dict(alpha=0.8, linewidth=0.6),
        whiskerprops=dict(linewidth=0.6),
        capprops=dict(linewidth=0.6),
        medianprops=dict(linewidth=0.6),
    )
    
    #sns.stripplot(x=var, y='height', data=sel1r, dodge=True, alpha=0.9, jitter=0.2, size=4, order=yorder, palette=my_cols, linewidth=1, edgecolor='gray', hue_order= hueorder,hue='experiment')
    #ax=sns.boxplot(x=var, y='height', data=sel1r, whis=np.inf ,order=yorder, hue_order= hueorder,hue='experiment', palette=my_cols, boxprops=dict(alpha=0.8))

    #ax = sns.boxplot(
    #    x=var, y='height', data=sel1r, whis=np.inf,
    #    order=yorder, hue_order= hueorder,hue='experiment', palette=my_cols
    #    )
    for patch in ax.patches:
        patch.set_alpha(0.8)

    for spine in ax.spines.values():
        spine.set_linewidth(0.6)

    
    plt.tick_params(bottom=False)
    plt.grid(True)
    #plt.xlim(0,100)
    plt.tick_params(axis='y', labelsize=20)
    plt.tick_params(axis='x', labelsize=20)
    if var == 'sca':
        plt.xlim(0,100)
        plt.xlabel('snow cover fraction [%]', fontsize=22)
    if var == 'snw':
        plt.xlim(0,1000)
        plt.xlabel('snow water equivalent [mm]', fontsize=22)
    if var == 'snowday':
        plt.xlim(0,32)
        plt.xlabel('snow days [days/month]', fontsize=22)
    plt.ylabel('height [m]', fontsize=22)
    plt.title(title, color='k', fontsize=22) 

    handles, labels = ax.get_legend_handles_labels()
    if var == 'snw':
        l = plt.legend(handles[0:4], labels[0:4], loc='lower right', borderaxespad=0.5, fontsize=14, markerscale=2)
    else:
        l = plt.legend(handles[0:4], labels[0:4], loc=2, borderaxespad=0.5, fontsize=14, markerscale=2)  #bbox_to_anchor=(1.05, 1)
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches='tight')    
    
    return


def boxplot_all_exp_regions_timeslices_grid(
    df_neu,
    df_hist_rcp85,
    plotdir,
    title,
    regions,
    region_titles,
    times,
    var,
):
    """Create one figure with rows=regions and cols=time slices.

    Parameters
    ----------
    df_neu : pandas.DataFrame
        Must contain columns: 'height', 'region', 'timeslice', 'experiment', and `var`.
        Should include future time slices with experiments rcp26/rcp45/rcp85.
    df_hist_rcp85 : pandas.DataFrame
        Historical baseline to be added to every time slice column.
        Must contain same columns as `df_neu` but with experiment 'rcp85-1971-2000'.
    plotdir : str
        Output directory.
    title : str
        Figure title.
    regions : list[str]
        Region codes (row order).
    region_titles : list[str]
        Human-readable region names (same length as regions).
    times : list[str] | tuple[str, ...]
        Time slice labels (column order), e.g. ('2021-2050','2069-2098').
    var : str
        Variable name plotted on x-axis (must be a column in the input frames).
    """

    my_cols = {
        'rcp85': cm.roma(0.00),
        'rcp45': cm.lajolla(0.7),
        'rcp26': cm.roma(1.00),
        'rcp85-1971-2000': cm.grayC(0.8),
    }
    yorder = ['3000', '2500', '2000', '1500', '1000', '500']
    hueorder = ['rcp85', 'rcp45', 'rcp26', 'rcp85-1971-2000']

    if len(regions) != len(region_titles):
        raise ValueError('regions and region_titles must have the same length')

    nrows = len(regions)
    ncols = len(times)
    # A4 page size in inches (matplotlib uses inches for figsize)
    a4_portrait = (8.27, 11.69)
    a4_landscape = (11.69, 8.27)
    figsize = a4_landscape if ncols > nrows else a4_portrait

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, sharex=True, sharey=True)
    if nrows == 1 and ncols == 1:
        axes = np.array([[axes]])
    elif nrows == 1:
        axes = np.array([axes])
    elif ncols == 1:
        axes = np.array([[ax] for ax in axes])

    legend_handles = None
    legend_labels = None

    for col_idx, t in enumerate(times):
        selc = df_neu.loc[df_neu['timeslice'] == t]
        sel = pd.concat([selc, df_hist_rcp85], ignore_index=True)

        for row_idx, (region, region_name) in enumerate(zip(regions, region_titles)):
            ax = axes[row_idx, col_idx]
            sel_region = sel.loc[sel['region'] == region]

            if sel_region.empty:
                ax.set_axis_off()
                ax.text(0.5, 0.5, f'No data\n{region_name} / {t}', ha='center', va='center', transform=ax.transAxes)
                continue

            sns.stripplot(
                x=var,
                y='height',
                data=sel_region,
                dodge=True,
                alpha=0.9,
                jitter=0.3,
                size=1,
                order=yorder,
                palette=my_cols,
                linewidth=0.3,
                edgecolor='gray',
                hue_order=hueorder,
                hue='experiment',
                ax=ax,
            )

            box_ax = sns.boxplot(
                x=var,
                y='height',
                data=sel_region,
                whis=np.inf,
                order=yorder,
                hue_order=hueorder,
                hue='experiment',
                palette=my_cols,
                linewidth=0.6,
                boxprops=dict(alpha=0.8, linewidth=0.6),
                whiskerprops=dict(linewidth=0.6),
                capprops=dict(linewidth=0.6),
                medianprops=dict(linewidth=0.6),
                ax=ax,
            )

            for patch in box_ax.patches:
                patch.set_alpha(0.8)

            for spine in ax.spines.values():
                spine.set_linewidth(0.6)

            ax.grid(True)
            ax.tick_params(bottom=False)
            ax.tick_params(axis='y', labelsize=12)
            ax.tick_params(axis='x', labelsize=12)

            # Capture legend once, then remove per-axis legends.
            if legend_handles is None:
                legend_handles, legend_labels = ax.get_legend_handles_labels()
            leg = ax.get_legend()
            if leg is not None:
                leg.remove()

            if row_idx == 0:
                ax.set_title(t, fontsize=12)
            if col_idx == 0:
                ax.set_ylabel('height [m]', fontsize=12)
                ax.text(
                    -0.26,
                    0.5,
                    region_name,
                    transform=ax.transAxes,
                    rotation=90,
                    va='center',
                    ha='center',
                    fontsize=12,
                )
            else:
                ax.set_ylabel('')
                ax.tick_params(axis='y', labelleft=False)

            if row_idx == nrows - 1:
                if var == 'sca':
                    ax.set_xlabel('snow cover fraction [%]', fontsize=14)
                elif var == 'snw':
                    ax.set_xlabel('snow water equivalent [mm]', fontsize=14)
                elif var == 'snowday':
                    ax.set_xlabel('snow days [days/month]', fontsize=14)
                else:
                    ax.set_xlabel(var, fontsize=14)
            else:
                ax.set_xlabel('')
                ax.tick_params(axis='x', labelbottom=False)

            if var == 'sca':
                ax.set_xlim(0, 100)
            elif var == 'snw':
                ax.set_xlim(0, 1000)
            elif var == 'snowday':
                ax.set_xlim(0, 32)

    #fig.suptitle(title, fontsize=18, y=0.995)
    if legend_handles is not None and legend_labels is not None:
        fig.legend(
            legend_handles[:4],
            legend_labels[:4],
            # place legend below the axes area
            loc='lower center',
            ncol=4,
            bbox_to_anchor=(0.55, +0.035),
            fontsize=12,
            markerscale=2,
            frameon=False,
        )

    OutFile = os.path.join(plotdir, f'Boxplot_{var}_ALLREGIONS_ALLTIMES.png')
    print('Plot will be : ', OutFile)
    # reserve space at the bottom for the legend
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(OutFile, bbox_inches='tight')

    return
