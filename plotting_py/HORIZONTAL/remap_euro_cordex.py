#!/usr/bin/env python3
import os
import glob
import pandas as pd
import os
import glob
import shutil

#import xarray as xr
import numpy as np
#from pyhomogenize import open_xrdataset
import seaborn as sns
#
from cmcrameri import cm
import subprocess


class CdoWrapper:
    def __init__(self):
        self.forceOutput = True

    def setgrid(self, grid, input, output=None):
        if output is None:
            output = f"{input}.setgrid.nc"
        cmd = ["cdo", f"setgrid,{grid}", input, output]
        subprocess.run(cmd, check=True)
        return output

    def remapcon(self, grid, input, output):
        cmd = ["cdo", f"remapcon,{grid}", input, output]
        subprocess.run(cmd, check=True)
        return output


cdo = CdoWrapper()
forceCDO = True


def remap(RCM, datadir, tmpdir, infile, outfilename, griddir, grid):

    if RCM == 'ICTP':
        gridr=griddir+'/grid_ICTP-RegCM4-6.txt'
        print('ICTP-remap')
    elif RCM == 'CNRM':
        print('CNRM-remap')
        gridr=griddir+'/grid_CNRM-ALADIN63.txt'
    else:
        print('grid not found')
    
    outfile=os.path.join(datadir,outfilename)
    file=os.path.join(tmpdir,infile)
    
    print('grid used: ', gridr)
    
    f1=cdo.setgrid(gridr,input=file)
    cdo.remapcon(grid,input=f1, output=outfile)
    return

def setgrid(datadir, tmpdir, infile, outfilename, grid):
    outfile=os.path.join(datadir,outfilename)
    file=os.path.join(tmpdir,infile)
    cdo.setgrid(grid,input=file, output=outfile)
    return


home= '/home/g/g300047/SCRIPTS/github/snow-research/plotting_py/HORIZONTAL'
griddir=home.replace('plotting_py/HORIZONTAL','grid')
grid=home.replace('plotting_py/HORIZONTAL','grid/EUR11-grid.txt')


############################################
#
# make adjustments according to your choice SNW/snw or SNOWDAY ..
#
######################

database='/work/ch0636/g300047/SNOW-RESEARCH/HORIZONTAL-NA'
os.makedirs(database, exist_ok=True)
print(f"Directory ready: {database}")
#the remapped data is stored in the following directory:
datadir=database+'/SNOWDAY-NA'
os.makedirs(datadir, exist_ok=True)
print(f"Directory ready: {datadir}")

#outdatadir=database+'/SNW-timeslice'
#os.makedirs(outdatadir, exist_ok=True)
#print(f"Directory ready: {outdatadir}")

# row input data is stored in the following directory:
tmpdir="/work/ch0636/g300047/INDICES-SP-KB/Euro-Cordex-Indices/snow/snowday_timeseries-na/tmp"

# these files will get remapped to the grid specified in the variable "grid" 
# and stored in the directory specified in the variable "datadir"    
sims = sorted(glob.glob(os.path.join(tmpdir, "*.nc")))
#
var="sd"

###########################################

# remap:

for sim in sims:
    filename = os.path.basename(sim)
    if var == 'snw':
        outfilename=filename.split('_')[1]+'_'+filename.split('_')[2]+'_'+filename.split('_')[0]+'_snw_'+filename.split('_')[7]+'_'+filename.split('_')[8]+'_'+filename.split('_')[9]+'_'+filename.split('_')[10]+'.nc'
    else:
        outfilename=filename.split('_')[1]+'_'+filename.split('_')[2]+'_'+filename.split('_')[0]+'_'+filename.split('_')[5]+'_'+filename.split('_')[8]+'_'+filename.split('_')[9]+'_'+filename.split('_')[10]+'_'+filename.split('_')[11]+'.nc'
    print(outfilename)
    # need to adjusted to your path:
    tmp=filename.split('_')[10]
    RCM=tmp.split('-')[0]
    print(RCM)
    if RCM == 'ICTP':
        print('remap: ',RCM, ' , ', outfilename)
        remap(RCM, datadir, tmpdir, filename, outfilename,griddir,grid)    
    elif RCM == 'MPI':
        print('set grid: ',RCM, ' , ', outfilename)
        setgrid(datadir, tmpdir, filename, outfilename,grid)
    elif RCM == 'CNRM':
        print('remap: ',RCM, ' , ', outfilename)
        remap(RCM, datadir, tmpdir, filename, outfilename,griddir,grid)
    else:
        print('set grid: ',RCM, ' , ', outfilename)
        setgrid(datadir, tmpdir, filename, outfilename,grid)


