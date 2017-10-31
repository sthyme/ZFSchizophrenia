#!/bin/bash
#SBATCH -J calc_overlap
#SBATCH --array=1,5%5      ## --array=X-Y%Z, where X-Y is the range of job
                           ## numbers to run, and Z is the max that can run
                           ## at one time. This must exactly match the number
                           ## of samples in the file list.
#SBATCH -n 4               ## num threads
#SBATCH -N 1               ## All cores on one node.
#SBATCH --mem=10240         ## 10G of RAM
#SBATCH -t 0-06:00         ## Time job can run (6 hour)
#SBATCH -p serial_requeue  ## Queue
#SBATCH -o run_log/calc_overlap.%A_%a.out.log  ## requires that the run_log directory already exist in the same folder of this script.
#SBATCH -e run_log/calc_overlap.%A_%a.err.log

source new-modules.sh
module load Anaconda3/2.1.0-fasrc01
source activate python_env1

file_list="./index_list.txt" ## contains the start and end indices of the images for each sub-job. 

f_dir="../Images/" ## directory that contains the images of interest. In this script, all directory names need to end with a "/".
out_dir="../Results/"
py_script="./calc_similarity_matrix.py"
mask_f="../Masks/whole_brain_mask_no_SpinalCord" ## if don't want to use mask, this can be set to "None". Otherwise must provide the path to a dill dumped file.
st_ed=`sed -n "$SLURM_ARRAY_TASK_ID"p "${index_list}"`
thres="50"
pre="similarity_matrix_${st_ed}" ## prefix to use for the saved result files

mkdir -p ${out_dir}

python -u ${py_script} -f_dir ${f_dir} -dil "[2,4,4]" -out_dir ${out_dir} -pre ${pre} -mask_f ${mask_f} -st_ed ${st_ed} -sym False -thres ${thres}