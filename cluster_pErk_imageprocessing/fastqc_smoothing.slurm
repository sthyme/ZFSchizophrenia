#!/bin/bash

#SBATCH -p serial_requeue # Partition to submit to

#SBATCH -n 1 # Number of cores requested
#SBATCH --exclusive
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-socket=1
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 15 # Runtime in minutes
#SBATCH --mem=4000 # Memory per cpu in MB (see also --mem-per-cpu)
#SBATCH --job-name=arrayJob
#SBATCH --array=100-187
#SBATCH -o hostname_%A_%a.out # Standard out goes to this file
#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname

/n/schierfs1/projects/ImageRegistration/Fiji.app/ImageJ-linux64 -macro /n/schierfs1/projects/ImageRegistration/Fiji.app/scripts/PrepareStacksForMAPMapping_cluster.m "Ref20131120pt14pl2_snap91homhetfsnap91hethomf_2017_06_12__23_35_56__p$SLURM_ARRAY_TASK_ID warp_m0g80c4e1e-1x52r3.nrrd /n/regal/schier_lab/microscopyjunemay2017/SNAP91homhetfSNAP91hethomf/smoothedtiffs/"


#source new-modules.sh; module load fastqc
#fastqc --casava -o fastqc_reports A01_R1.pair.fastq.gz
