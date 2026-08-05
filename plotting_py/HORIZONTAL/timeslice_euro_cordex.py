
#!/usr/bin/env python3
import os
import glob
import pandas as pd
import shutil
import numpy as np
import seaborn as sns
from cmcrameri import cm
import subprocess
import xarray as xr  # needed by seltimeslice()
from pyhomogenize import open_xrdataset, save_xrdataset
import scipy.stats as sts


class CdoWrapper:
    def __init__(self):
        self.forceOutput = True

    def selyear(self, years, input, output):
        cmd = ["cdo", f"selyear,{years}", input, output]
        subprocess.run(cmd, check=True)
        return output

    def timmean(self, input, output):
        cmd = ["cdo", "timmean", input, output]
        subprocess.run(cmd, check=True)
        return output

cdo = CdoWrapper()
forceCDO = True


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




#home= '/home/g/g300047/SCRIPTS/github/snow-research/plotting_py/HORIZONTAL'
#griddir=home.replace('plotting_py/HORIZONTAL','grid')
#grid=home.replace('plotting_py/HORIZONTAL','grid/EUR11-grid.txt')


############################################
#
# make adjustments according to your choice SNW/snw or SNOWDAY ..
#
######################

database='/work/ch0636/g300047/SNOW-RESEARCH/HORIZONTAL-NA'
os.makedirs(database, exist_ok=True)
print(f"Directory ready: {database}")
#the remapped data is stored in the following directory:
datadir=database+'/SNW-NA'
os.makedirs(datadir, exist_ok=True)
print(f"Directory ready: {datadir}")

outdatadir=database+'/SNW-timeslice'
os.makedirs(outdatadir, exist_ok=True)
print(f"Directory ready: {outdatadir}")

#
var="snw"

###########################################
sims_remaped = sorted(glob.glob(os.path.join(datadir, "*rcp26*.nc")))

for sim in sims_remaped:
    
    filename=sim.split('/')[7]
    outfilename=filename.split('_')[4]+'_'+filename.split('_')[5]+'_'+filename.split('_')[6]+'_'+filename.split('_')[7]
    print(outfilename)
    tmp=filename.split('_')[7]
    RCM=tmp.split('.')[0]
    print(RCM)
    
    seltimeslice(sim,outfilename,outdatadir,var=var) 

