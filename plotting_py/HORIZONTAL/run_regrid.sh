#!/bin/ksh                                                                                                                                       
#SBATCH --job-name=regrid         # Specify job name                                                                                    
#SBATCH --partition=compute               # Specify partition name                                                                               
#SBATCH --nodes=1                         # Specify max. number of tasks to be invoked                                                           
#SBATCH --ntasks-per-node=256                                                                                                                    
#SBATCH --mem-per-cpu=3940                                                                                                                       
#SBATCH --time=08:00:00                   # Set a limit on the total run time                                                                    
#SBATCH --mail-type=FAIL                  # Notify user by email in case of job failure                                                          
#SBATCH --account=ch0636                  # Charge resources on this project account                                                             
#SBATCH --output=/scratch/g/g300047/snow/calculate_na_regrid.log                                                                                 
#SBATCH --error=/scratch/g/g300047/snow/calculate_na_regrid.err                                                                                  

# Bind your OpenMP threads                                                                                                                       
export OMP_NUM_THREADS=4
export KMP_AFFINITY=verbose,granularity=fine,scatter
# limit stacksize ... adjust to your programs need                                                                                               
# and core file size                                                                                                                             
ulimit -s 204800
ulimit -c 0
export OMP_STACKSIZE=128M

###################################################                                                                                              
#Execute programs                                                                                                                                
###################################################                                                                                              
#                                                                                                                                                
#                                                                                                                                                

python /home/g/g300047/SCRIPTS/github/snow-research/plotting_py/HORIZONTAL/remap_euro_cordex.py

