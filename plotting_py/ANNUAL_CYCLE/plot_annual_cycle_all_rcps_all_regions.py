#! /usr/bin/python
# coding: utf-8
import sys
from pathlib import Path


# Allow running this script from any working directory by ensuring the repo
# root (the parent of `plotting_py/`) is on sys.path.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

try:
    import matplotlib.pyplot as plt
except Exception as exc:
    raise SystemExit(
        "Failed to import matplotlib. This is usually caused by a NumPy/Matplotlib binary mismatch "
        "(e.g. NumPy 2.x with extensions built against NumPy 1.x).\n\n"
        "Recommended fix: run this script inside the conda env defined in snow310.yml, e.g.:\n"
        "  conda run -n snow310 python plotting_py/ANNUAL_CYCLE/plot_annual_cycle_all_rcps_all_regions.py\n\n"
        "Or ensure your active environment uses numpy<2.\n\n"
        f"Original error: {exc}"
    )
import os
import pandas as pd
import glob
import numpy as np
import seaborn as sns
from cmcrameri import cm
from plotting_py.TIMESERIES.colortable import colortable
from plotting_py.TIMESERIES.design_matrix_tool import design_df_mean
#from matplotlib.transforms import ScaledTranslation


# Font sizes for plots
AXIS_LABEL_FONTSIZE = 12
TICK_LABEL_FONTSIZE = 12
FACET_TITLE_FONTSIZE = 12
LEGEND_FONTSIZE = 12
LEGEND_TITLE_FONTSIZE = 12
LEGEND_BBOX_Y = -0.14

# Percentile band ("prediction interval") settings
PERCENTILE_INTERVAL = 95  # 95% band => 2.5th to 97.5th percentile
BAND_ALPHA = 0.20

# Month handling: enforce Sep→Aug order to match the intended water year labels.
_MONTH_ORDER = ['Sep', 'Oct', 'Okt', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
_MONTH_LABELS_SHORT = ['S', 'O', 'N', 'D', 'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A']


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
    
    # seaborn<0.12 does not support the `errorbar=` API.
    def _seaborn_supports_errorbar() -> bool:
        try:
            major, minor = (int(x) for x in sns.__version__.split('.')[:2])
        except Exception:
            return False
        return (major, minor) >= (0, 12)

    # Normalize month to a numeric index (Sep=0 ... Aug=11). This keeps the
    # x-axis order stable and makes manual fill_between work reliably.
    df = df.copy()
    if 'month' not in df.columns:
        raise ValueError("Expected column 'month' in input dataframe")

    if pd.api.types.is_numeric_dtype(df['month']):
        # Assume 1..12, map Sep(9)->0 ... Aug(8)->11
        df['month_idx'] = (df['month'].astype(int) - 9) % 12
    else:
        month_map = {
            'Sep': 0,
            'Oct': 1,
            'Okt': 1,
            'Nov': 2,
            'Dec': 3,
            'Jan': 4,
            'Feb': 5,
            'Mar': 6,
            'Apr': 7,
            'May': 8,
            'Jun': 9,
            'Jul': 10,
            'Aug': 11,
        }
        df['month_idx'] = df['month'].map(month_map)
        if df['month_idx'].isna().any():
            unknown = sorted(set(df.loc[df['month_idx'].isna(), 'month'].astype(str)))
            raise ValueError(f"Unknown month labels in 'month' column: {unknown}")

    relplot_kwargs = dict(
        x='month_idx',
        y=var,
        data=df,
        err_style="band",
        estimator=np.median,
        hue='rcp_timeslice',
        hue_order=[
            'rcp26_1971-2000', 'rcp26_2021-2050', 'rcp26_2069-2098',
            'rcp45_1971-2000', 'rcp45_2021-2050', 'rcp45_2069-2098',
            'rcp85_1971-2000', 'rcp85_2021-2050', 'rcp85_2069-2098',
        ],
        palette=colors,
        kind='line',
        col='exp',
        col_order=['rcp26', 'rcp45', 'rcp85'],
        row='region',
        row_order=['Alps', 'Eastern E.', 'Iberian P.', 'Scandinavia'],
        height=2,
        aspect=1.5,
        facet_kws={'sharey': False, 'sharex': True},
    )

    # Use seaborn's percentile interval when available; otherwise add a manual
    # percentile band (older seaborn only supports CI, which is not what we want).
    supports_errorbar = _seaborn_supports_errorbar()
    if supports_errorbar:
        relplot_kwargs['errorbar'] = ('pi', PERCENTILE_INTERVAL)
    else:
        relplot_kwargs['ci'] = None

    g = sns.relplot(**relplot_kwargs)

    if not supports_errorbar:
        # Manual PI bands for older seaborn
        regions = relplot_kwargs['row_order']
        exps = relplot_kwargs['col_order']
        hue_levels = relplot_kwargs['hue_order']
        q_low = (100 - PERCENTILE_INTERVAL) / 2.0
        q_high = 100 - q_low
        month_positions = np.arange(12)

        axes = np.asarray(g.axes)
        if axes.ndim == 1:
            axes = axes.reshape(-1, 1)
        for row_idx, region in enumerate(regions):
            for col_idx, exp in enumerate(exps):
                ax = axes[row_idx, col_idx]
                sub = df.loc[(df['region'] == region) & (df['exp'] == exp)]
                if sub.empty:
                    continue

                for hue_level in hue_levels:
                    sub_h = sub.loc[sub['rcp_timeslice'] == hue_level]
                    if sub_h.empty:
                        continue

                    lows = []
                    highs = []
                    for m in month_positions:
                        vals = sub_h.loc[sub_h['month_idx'] == m, var].to_numpy()
                        vals = vals[np.isfinite(vals)]
                        if vals.size == 0:
                            lows.append(np.nan)
                            highs.append(np.nan)
                        else:
                            lows.append(np.nanpercentile(vals, q_low))
                            highs.append(np.nanpercentile(vals, q_high))

                    color = colors.get(hue_level, None)
                    ax.fill_between(month_positions, lows, highs, color=color, alpha=BAND_ALPHA, linewidth=0)

    # X-axis month labels (Sep→Aug)
    for ax in g.axes.flatten():
        ax.set_xticks(np.arange(12))
        ax.set_xticklabels(_MONTH_LABELS_SHORT, fontsize=TICK_LABEL_FONTSIZE)
        ax.set_xlim(-0.5, 11.5)
    # Only one y-label for the whole figure (saves space)
    g.set_axis_labels(xname, "", fontsize=AXIS_LABEL_FONTSIZE)
    g.set_titles(row_template='{row_name}', col_template='{col_name}', size=FACET_TITLE_FONTSIZE)

    # Remove any leftover per-axes y-labels and add a single figure-level one.
    for ax in g.axes.flatten():
        ax.set_ylabel("")
    ylabel_text = g.fig.text(
        0.02,
        0.5,
        yname,
        va='center',
        rotation='vertical',
        fontsize=AXIS_LABEL_FONTSIZE,
    )

    for ax in g.axes.flatten():
        ax.tick_params(axis='both', which='major', labelsize=TICK_LABEL_FONTSIZE)

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

    sns.move_legend(
        g,
        'lower center',
        scatterpoints=1,
        bbox_to_anchor=(0.45, LEGEND_BBOX_Y),
        fancybox=True,
        shadow=True,
        ncol=3,
    )
    if g.legend is not None:
        for text in g.legend.get_texts():
            text.set_fontsize(LEGEND_FONTSIZE)
        if g.legend.get_title() is not None:
            g.legend.get_title().set_fontsize(LEGEND_TITLE_FONTSIZE)

    plotname = os.path.join(plotdir, f"all_regions_{var}_median_annualcycle_all_rcps.png")
    print(f"Saving plot to {plotname}")
    extra_artists = [ylabel_text]
    if g.legend is not None:
        extra_artists.append(g.legend)
    plt.savefig(plotname, bbox_inches="tight", bbox_extra_artists=extra_artists)

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
   

