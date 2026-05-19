#!/usr/bin/env python3

import os
import pandas as pd

import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xarray as xr
import cftime

from cdo import *
cdo = Cdo()  
cdo.forceOutput = True
forceCDO = True

import dask
from dask.distributed import Client
import scipy.stats as sts
import xarray as xr
import dask
from pyhomogenize import open_xrdataset, save_xrdataset

import cordex
from cartopy import crs as ccrs
import cartopy.feature as cf

import matplotlib
font = {
    'family' : 'sans-serif',
    'weight' : 'normal',
    'size'   : 15,
}

matplotlib.rc('font', **font)

def savefig(plot, name, dpi=300, **kwargs):
    plot.savefig(name, dpi=dpi, **kwargs)

def remap(RCM, datadir, tmpdir, infile, griddir, grid):

    if RCM == 'ICTP':
        gridr=griddir+'/grid_ICTP-RegCM4-6.txt'
        print('ICTP-remap')
    elif RCM == 'CNRM':
        print('CNRM-remap')
        gridr=griddir+'/grid_CNRM-ALADIN63.txt'
    else:
        print('grid not found')
    
    outfile=os.path.join(datadir,infile)
    file=os.path.join(tmpdir,infile)
    
    print('grid used: ', gridr)
    
    f1=cdo.setgrid(gridr,input=file)
    cdo.remapcon(grid,input=f1, output=outfile)
    return

def setgrid(datadir, tmpdir, infile, grid):
    outfile=os.path.join(datadir,infile)
    file=os.path.join(tmpdir,infile)
    cdo.setgrid(grid,input=file, output=outfile)
    return

def calculate_pvalue(ds, ds_ref, var):
    print("Do Mann-Whitney-U-Test.")
    ds_ref = ds_ref.chunk(dict(time=-1))
    ds = ds.chunk(dict(time=-1))
    
    def _mannwhitneyu(sample1, sample2):
        return sts.mannwhitneyu(
            sample1, 
            sample2, 
            nan_policy = "omit",
        )[1]
    da = xr.apply_ufunc(
        _mannwhitneyu,
        ds_ref[var],
        ds[var],
        input_core_dims=[["time"], ["time"]],
        vectorize=True,
        dask="parallelized",
        output_dtypes = ["float32"],
        keep_attrs = True,
    ).compute()
    ds["p_value"] = da
    ds["significance"] = xr.where(da < 0.05, 1, 0)
    ds["significance"].attrs = ds["p_value"].attrs
    return ds

def seltimeslice(sim,outfilename,outdatadir,var):
    '''
    Select timeslice, output annual files (30 timesteps)
    calculate mean over timeslice 
    calculate difference
    calculate significance of change
    '''
    
    for timeslice in ('1972/2001','2070/2099', '2022/2051'):
        timeslicen=timeslice.replace('/','_')
        outfile=os.path.join(outdatadir,timeslicen+'_'+outfilename)
        print('sel time slice : ',sim)
        cdo.selyear(timeslice, input=sim, output=outfile)
        
        outfilemean=os.path.join(outdatadir,'MEAN_'+timeslicen+'_'+outfilename)
        cdo.timmean(input=outfile, output=outfilemean)
        
        print(outfile)
        print('calculate significance')
        
        if timeslice != '1972/2001':
            ds = xr.open_mfdataset(outfile, decode_times=False)
            ds_ref_c = ds_ref.copy()
            ds = ds.fillna(0)
            print('len(ds.time): ',len(ds.time))
            print('len(ds_ref_c.time): ',len(ds_ref_c.time))
            if len(ds.time) < len(ds_ref_c.time):
                ds_ref_c = ds_ref_c.isel(time=slice(0,len(ds.time)))
                print('len(ds_ref_c.time): ',len(ds_ref_c.time))
            ds_ref_c["time"] = ds.time
            ds_ref_c = ds_ref_c.fillna(0)
            outfilesig=os.path.join(outdatadir,'significance_'+timeslicen+'_'+outfilename)

            ds_p = calculate_pvalue(ds, ds_ref_c, var)           
            print('outfilemean: ',outfilemean)
            ds_mean = xr.open_mfdataset(outfilemean, decode_times=False)
            del ds_mean["time"]
            if "time_bnds" in ds_mean.data_vars:
                del ds_mean["time_bnds"]
            ds_mean = ds_mean.squeeze()
            ds_p[var+"_diff"] = ds_mean[var] - ds_hist_mean[var]
            save_xrdataset(ds_p, outfilesig)
            print("File written: ", outfilesig)
        
        else:
            print('read historical')
            ds_ref = xr.open_mfdataset(outfile, decode_times=False)
            ds_hist_mean = xr.open_mfdataset(outfilemean, decode_times=False) 
            del ds_hist_mean["time"]
            if "time_bnds" in ds_hist_mean.data_vars:
                del ds_hist_mean["time_bnds"]
            ds_hist_mean = ds_hist_mean.squeeze()
    return

def calculate_ensemble_robustness(
        da_diff,
        da_sig,
        ensemble_dim,
        compute=True,
):
    def _where(
            da,
            rel_op,
            rel_value=0,
            then_value=1,
            else_value=0,
    ):
        if rel_op == ">":
            return xr.where(da > rel_value, then_value, else_value)
        if rel_op == "<":
            return xr.where(da < rel_value, then_value, else_value)
        if rel_op == "==":
            return xr.where(da == rel_value, then_value, else_value)
        raise("relational operator {} not known.").format(rel_op)

    def _percentage(da, da_ref, dim):
        da_s = da.sum(dim=dim)
        da_c = da_ref.count(dim=dim)
        return xr.where(da_c > 0, da_s / da_c, np.nan)
    
    diff_p = _where(da_diff, ">")
    diff_n = _where(da_diff, "<")
    #diff_0 = _where(ds[diff], "==")
    diff_p_p = _percentage(diff_p, da_diff, ensemble_dim)
    diff_n_p = _percentage(diff_n, da_diff, ensemble_dim)
    #diff_0_p = _percentage(diff_0, ds[diff], ensemble_dim)

    sig_p = _where(diff_p, "==", rel_value=1, then_value=da_sig)
    sig_n = _where(diff_n, "==", rel_value=1, then_value=da_sig)
    #sig_0 = _where(diff_0, "==", rel_value=1, then_value=ds[sig])
    sig_p_p = _percentage(sig_p, da_diff, ensemble_dim)
    sig_n_p = _percentage(sig_n, da_diff, ensemble_dim)
    #sig_0_p = _percentage(sig_0, ds[diff], ensemble_dim)

    da = xr.where(((diff_p_p >= 2/3) & (sig_p_p >= 1/2)), 1, 0)
    da = xr.where(((diff_n_p >= 2/3) & (sig_n_p >= 1/2)), -1, da)
    if compute is True:
        da = da.compute()
    return da

def ensemblemean_exp(outdatadir, var):
    ''' calculate mean for each scenario'''
    for timeslice in ['1972_2001', '2022_2051', '2070_2099']:
        for exp in ['rcp26','rcp45','rcp85']:
            outputfile=os.path.join(outdatadir,'ENS_MEAN_'+timeslice+'_'+exp+'.nc')
            ensemble_mean_files = glob.glob(outdatadir+'MEAN_'+timeslice+'*'+exp+'*.nc')
           
            cdo.ensmean(input=ensemble_mean_files, output=outputfile)
            print('Ensemble mean is calculated:', outputfile)
            if timeslice != "1972_2001":
                
                ensemble_sig_files = glob.glob(outdatadir+'significance_'+timeslice+'*'+exp+'*.nc')
                                               
                datasets = []
                for ifile in ensemble_sig_files:
                    ds = xr.open_mfdataset(ifile, decode_times=False) 
                    print('ifile =', ifile)
                    #
                    filename=ifile.split('/')[7]
                    #significance_2022_2051_MPI-M-MPI-ESM-LR_rcp85_r3i1p1_CLMcom-ETH-COSMO-crCLIM-v1.1.nc'
                    tmp=filename.split('_')[6]
                    RCM=tmp.split('.')[0]
                    print(RCM)
                    if RCM == "CLMcom-ETH-COSMO-crCLIM-v1":
                        print(RCM)
                        ds.attrs["driving_model_id"] = "MPI-ESM-LR"
                        ds.attrs["model_id"] = "CLMcom-ETH-COSMO-crCLIM-v1.1"
                        
                    gcm = ds.attrs["driving_model_id"]
                    rcm = ds.attrs["model_id"]
                    gcmrcm = "{}-{}".format(gcm, rcm)
                    ds = ds.assign_coords({"GCM-RCM": gcmrcm})
                    del ds[var]
                    del ds["p_value"]
                    del ds["time"]
                    if "time_bnds" in ds.data_vars:
                        del ds["time_bnds"]
                    ds["significance"] = ds["significance"].expand_dims("GCM-RCM")
                    ds[var+"_diff"] = ds[var+"_diff"].expand_dims("GCM-RCM")
                    datasets += [ds]
                ds_total = xr.concat(datasets, dim="GCM-RCM", data_vars=[var+"_diff", "significance"], compat="override", coords="minimal")
                #
                print('start to calculate ensemlbe robustness')
                ds_total["robustness"] = calculate_ensemble_robustness(
                    da_diff=ds_total[var+"_diff"],
                    da_sig=ds_total["significance"],
                    ensemble_dim="GCM-RCM",
                )
                ds_total[var+"_ensemble_diff"] = ds_total[var+"_diff"].mean(dim="GCM-RCM")
                outputfile=os.path.join(outdatadir,'ENS_ROBUSTNESS_'+timeslice+'_'+exp+'.nc')
                ds_total.to_netcdf(outputfile)
                print('Ensemble robustness is calculated:', outputfile)
            
    return

def directory_available(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def plot_3(
    ds_dict,
    var="",
    unit="",
    mode="",
    colors="",
    levels="",
    robustness=False,
    add_cbar = True,
    hatchcolor="k",
    output_path="",
    extend="neither",
):
    
    cordex_grid = cordex.cordex_domain("EUR-11")
    rotated_lat_lon = cordex_grid.rotated_latitude_longitude
    pole = (rotated_lat_lon.grid_north_pole_longitude, rotated_lat_lon.grid_north_pole_latitude)
    projection = ccrs.RotatedPole(*pole)
    
    title_fs = 18
    axis_label_fs = 26  # gridline lon/lat labels
    cbar_label_fs = 26
    cbar_tick_fs = 26

    fig, (ax1, ax2, ax3) = plt.subplots(
        ncols=3, nrows=1, subplot_kw={"projection": projection}, figsize=(20, 8),
    )
    axes = (ax1, ax2, ax3)
    pos = 0.03
    for ax in axes:
        gl = ax.gridlines(
            draw_labels={"bottom": "x", "left": "y", "top": False, "right": False},
            dms=True,
            x_inline=False, 
            y_inline=False,
            linewidth=0.5,
        )
        gl.xlabel_style = {"size": axis_label_fs}
        gl.ylabel_style = {"size": axis_label_fs}
        ax.coastlines(resolution="50m", color="black", linewidth=1)
        ax.add_feature(cf.BORDERS)
        ax.set_extent([-22,10,-16,21])
        
    for expts, ax in zip(ds_dict, axes):
        im = ds_dict[expts][var].plot(
            ax=ax,
            levels=levels,
            colors=colors,
            transform=projection,
            extend=extend,
            add_colorbar=False,
            #vmin=vmin,
            alpha=.8,  # bei diff
        )
        if robustness is True:
            rob_sel = ds_dict[expts]["robustness"]
            plt.rcParams.update({'hatch.color': hatchcolor})
            rob_sel = rob_sel.squeeze()
            significant = xr.where(rob_sel != 0, 1, 0).squeeze()
            significant.plot.contourf(
                ax=ax,
                levels=[-.5,.5],
                colors='none',
                hatches=[None, None, "//", "//"],
                add_colorbar=False,
                extend='both',
                transform=projection,
            )
        exp = expts.split("_")[0]
        ts = expts.split("_")[1]
        if var in ['sd', 'sd_ensemble_diff']:
            longvar='snow cover duration'
        elif var in ['snw', 'snw_ensemble_diff']:
            longvar='snow water equivalent'
        
        if mode == "absolut":
            s = "{} ({}), {}".format(longvar, exp, ts)
        elif mode == "diff": 
            s = "Mean change of {} \n Annual ({}), {}".format(longvar, exp, ts)
        
        ax.set_title(s+": ", fontdict={"fontsize": title_fs})
    if add_cbar is True:
        cbar_ax = fig.add_axes([0.13, pos, 0.7, 0.03])
        cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal")
        cbar.set_label(unit, fontsize=cbar_label_fs)
        cbar.ax.tick_params(labelsize=cbar_tick_fs)
    #savefig(plt, "{}/ensemble_mean_{}_{}_{}_YlGrBl.png".format(output_path, mode,var,ts))    
    savefig(plt, "{}/ensemble_mean_{}_{}_{}.png".format(output_path, mode, var, ts))
    print("Plot saved: {}/ensemble_mean_{}_{}_{}.png".format(output_path, mode, var, ts))  

    return plt

def plot_9(
    ds_dict,
    var="",
    mode="absolut",
    colors="",
    levels="",
    add_cbar=True,
    output_path="",
    extend="max",
    **kwargs,
    ):
    
    cordex_grid = cordex.cordex_domain("EUR-11", add_vertices=True)
    rotated_lat_lon = cordex_grid.rotated_latitude_longitude
    pole = (rotated_lat_lon.grid_north_pole_longitude, rotated_lat_lon.grid_north_pole_latitude)
    projection = ccrs.RotatedPole(*pole)
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(
        ncols=3, nrows=3, subplot_kw={"projection": projection}, figsize=(20,20),
    )
    title_fs = 24
    label_fs = 24
    cbar_label_fs = 24
    cbar_tick_fs = 24
    # Reduce whitespace between panels (keep enough bottom margin for the colorbar label)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.95, bottom=0.12, wspace=-0.46, hspace=0.04)
    axes = (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9)
    axes_grid = np.asarray(axes).reshape(3, 3)
    pos = 0.06
    cbar_y_offset = -0.01  # shift colorbar a tiny bit lower
    row_label_x_offset = -0.065  # shift row labels a tiny bit further left
    for idx, ax in enumerate(axes):
        # Only show x labels in the bottom row
        show_x = idx >= 6
        # Only show y labels in the first column
        show_y = idx % 3 == 0
        gl = ax.gridlines(
            draw_labels={
                "bottom": "x" if show_x else False,
                "left": "y" if show_y else False,
                "top": False,
                "right": False,
            },
            dms=True,
            x_inline=False,
            y_inline=False,
            linewidth=0.5,
        )
        gl.xlabel_style = {"size": label_fs}
        gl.ylabel_style = {"size": label_fs}
        ax.coastlines(resolution="50m", color="black", linewidth=1)
        ax.add_feature(cf.BORDERS)
        ax.set_extent([-22,10,-16,21])

    # Map the input dict to a fixed 3x3 layout:
    #   columns = RCPs, rows = time slices
    def _split_key(key):
        parts = str(key).split("_", 1)
        if len(parts) != 2:
            raise ValueError(f"plot_9 expects ds_dict keys like 'rcp85_2021-2050', got: {key!r}")
        return parts[0], parts[1]

    exps = []
    tss = []
    for k in ds_dict.keys():
        exp_k, ts_k = _split_key(k)
        exps.append(exp_k)
        tss.append(ts_k)

    exp_order_default = ["rcp26", "rcp45", "rcp85"]
    exp_order = [e for e in exp_order_default if e in set(exps)] + sorted(set(exps) - set(exp_order_default))
    ts_order = sorted(set(tss), key=lambda s: int(str(s).split("-")[0]) if str(s).split("-")[0].isdigit() else str(s))

    im = None
    for r, ts in enumerate(ts_order[:3]):
        for c, exp in enumerate(exp_order[:3]):
            ax = axes_grid[r, c]
            key = f"{exp}_{ts}"
            if key not in ds_dict:
                ax.set_visible(False)
                continue

            im = ds_dict[key][var].plot(
                ax=ax,
                levels=levels,
                colors=colors,
                transform=projection,
                extend=extend,
                add_colorbar=False,
            )

            # Titles: only the first row gets RCP titles
            if r == 0:
                ax.set_title(exp, fontdict={"fontsize": title_fs})
            else:
                ax.set_title("")

    # Row labels (time slices) as vertical text on the left
    for r, ts in enumerate(ts_order[:3]):
        ax0 = axes_grid[r, 0]
        if not ax0.get_visible():
            continue
        bbox = ax0.get_position()
        y_center = (bbox.y0 + bbox.y1) / 2
        # Keep label close to the first-column panels even if margins/wspace change
        x_pos = bbox.x0 + row_label_x_offset
        fig.text(
            x_pos,
            y_center,
            ts,
            rotation=90,
            va="center",
            ha="center",
            fontsize=title_fs,
            clip_on=False,
        )
    #fig.suptitle("Ensemble mean snow cover duration (September to August)", y=0.92,fontsize=25)
    if add_cbar is True and im is not None:
        #cbar.set_label("Values - how2matplotlib.com", fontsize=16)
        cbar_ax = fig.add_axes([0.14, pos + cbar_y_offset, 0.74, 0.02])
        cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal")
        if var == 'sd':
            cbar.set_label("[ days / year ]", fontsize=cbar_label_fs)
        elif var == 'snw':
            cbar.set_label("[ mm ]", fontsize=cbar_label_fs)

        cbar.ax.tick_params(labelsize=cbar_tick_fs)
    
    savefig(
        plt,
        "{}/ensemble_mean_{}_all_oTT.png".format(output_path, var),
        bbox_inches="tight",
        pad_inches=0.1,
    )
    print("Plot saved: {}/ensemble_mean_{}_all_oTT.png".format(output_path, var))
    return plt  

def plot_6(
    ds_dict,
    var="",
    mode="",
    colors="",
    levels="",
    robustness=True,
    add_cbar=True,
    hatchcolor="k",
    output_path="",
    extend="neither",
):
    
    cordex_grid = cordex.cordex_domain("EUR-11", add_vertices=True)
    rotated_lat_lon = cordex_grid.rotated_latitude_longitude
    pole = (rotated_lat_lon.grid_north_pole_longitude, rotated_lat_lon.grid_north_pole_latitude)
    projection = ccrs.RotatedPole(*pole)
    
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(
        ncols=3, nrows=2, subplot_kw={"projection": projection}, figsize=(19, 13),
    )
    title_fs = 24
    axis_label_fs = 24  # gridline lon/lat labels
    cbar_label_fs = 24
    cbar_tick_fs = 24

    # Tight layout (column gaps are usually the biggest issue with Cartopy)
    fig.subplots_adjust(left=0.02, right=0.99, top=0.93, bottom=0.12, wspace=-0.46, hspace=0.06)

    axes = (ax1, ax2, ax3, ax4, ax5, ax6)
    axes_grid = np.asarray(axes).reshape(2, 3)
    pos = 0.06
    cbar_y_offset = -0.01  # shift colorbar a tiny bit lower
    row_label_x_offset = -0.065  # shift row labels a tiny bit further left

    for idx, ax in enumerate(axes):
        # Only show x labels in the bottom row
        show_x = idx >= 3
        # Only show y labels in the first column
        show_y = idx % 3 == 0
        gl = ax.gridlines(
            draw_labels={
                "bottom": "x" if show_x else False,
                "left": "y" if show_y else False,
                "top": False,
                "right": False,
            },
            dms=True,
            x_inline=False,
            y_inline=False,
            linewidth=0.5,
        )
        gl.xlabel_style = {"size": axis_label_fs}
        gl.ylabel_style = {"size": axis_label_fs}
        ax.coastlines(resolution="50m", color="black", linewidth=1)
        ax.add_feature(cf.BORDERS)
        ax.set_extent([-22, 10, -16, 21])

    # Map the input dict to a fixed 2x3 layout:
    #   columns = RCPs, rows = time slices
    def _split_key(key):
        parts = str(key).split("_", 1)
        if len(parts) != 2:
            raise ValueError(f"plot_6 expects ds_dict keys like 'rcp85_2021-2050', got: {key!r}")
        return parts[0], parts[1]

    exps = []
    tss = []
    for k in ds_dict.keys():
        exp_k, ts_k = _split_key(k)
        exps.append(exp_k)
        tss.append(ts_k)

    exp_order_default = ["rcp26", "rcp45", "rcp85"]
    exp_order = [e for e in exp_order_default if e in set(exps)] + sorted(set(exps) - set(exp_order_default))
    ts_order = sorted(
        set(tss),
        key=lambda s: int(str(s).split("-")[0]) if str(s).split("-")[0].isdigit() else str(s),
    )

    im = None
    for r, ts in enumerate(ts_order[:2]):
        for c, exp in enumerate(exp_order[:3]):
            ax = axes_grid[r, c]
            key = f"{exp}_{ts}"
            if key not in ds_dict:
                ax.set_visible(False)
                continue

            im = ds_dict[key][var].plot(
                ax=ax,
                levels=levels,
                colors=colors,
                transform=projection,
                extend=extend,
                add_colorbar=False,
                alpha=0.8,
            )

            if robustness is True:
                rob_sel = ds_dict[key]["robustness"]
                plt.rcParams.update({"hatch.color": hatchcolor})
                rob_sel = rob_sel.squeeze()
                significant = xr.where(rob_sel != 0, 1, 0).squeeze()
                significant.plot.contourf(
                    ax=ax,
                    levels=[-0.5, 0.5],
                    colors="none",
                    hatches=[None, None, "//", "//"],
                    add_colorbar=False,
                    extend="both",
                    transform=projection,
                )

            # Titles: only the first row gets RCP titles
            if r == 0:
                ax.set_title(exp, fontdict={"fontsize": title_fs})
            else:
                ax.set_title("")

    # Row labels (time slices) as vertical text on the left
    for r, ts in enumerate(ts_order[:2]):
        ax0 = axes_grid[r, 0]
        if not ax0.get_visible():
            continue
        bbox = ax0.get_position()
        y_center = (bbox.y0 + bbox.y1) / 2
        x_pos = bbox.x0 + row_label_x_offset
        fig.text(
            x_pos,
            y_center,
            ts,
            rotation=90,
            va="center",
            ha="center",
            fontsize=title_fs,
            clip_on=False,
        )

    #fig.suptitle("Ensemble mean snow cover duration (November - April)", y=0.92,fontsize=25)
    if add_cbar is True and im is not None:
        cbar_ax = fig.add_axes([0.14, pos + cbar_y_offset, 0.74, 0.03])
        cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal")
        # Keep existing default label but set font sizes
        if var == 'sd_ensemble_diff':
            cbar.set_label("[ days / year ]", fontsize=cbar_label_fs)
        elif var == 'snw_ensemble_diff':
            cbar.set_label("[ mm ]", fontsize=cbar_label_fs)
        cbar.ax.tick_params(labelsize=cbar_tick_fs)
    
    savefig(
        plt,
        "{}/ensemble_mean_diff_{}_all_oT_YlGrBl.png".format(output_path, var),
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return plt  
