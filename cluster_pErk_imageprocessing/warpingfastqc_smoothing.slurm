#!/bin/bash

#SBATCH -p serial_requeue # Partition to submit to

#SBATCH -n 1 # Number of cores requested
#SBATCH --exclusive
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-socket=1
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 10 # Runtime in minutes
#SBATCH --mem=4000 # Memory per cpu in MB (see also --mem-per-cpu)
#SBATCH --job-name=arrayJob
#SBATCH --array=192,194,195,196,161,162,163,36,37,166,167,168,177,179,223,64,193,66,67,68,197,164,222,165,224,225,226
#SBATCH -o hostname_%A_%a.out # Standard out goes to this file
#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname

/n/schierfs1/projects/ImageRegistration/Fiji.app/ImageJ-linux64 -macro /n/schierfs1/projects/ImageRegistration/Fiji.app/scripts/PrepareJacobianStacksForMAPMapping_cluster.m "jacobian_$SLURM_ARRAY_TASK_ID.nrrd /n/regal/schier_lab/srphz_luzpz_fxr1_hcn1_tle/warpingsmoothed/"

#source new-modules.sh; module load fastqc
#fastqc --casava -o fastqc_reports A01_R1.pair.fastq.gz
