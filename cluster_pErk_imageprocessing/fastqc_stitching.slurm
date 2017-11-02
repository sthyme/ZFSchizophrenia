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
#SBATCH --array=10-69
#SBATCH -o hostname_%A_%a.out # Standard out goes to this file
#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname

xvfb-run -a /n/schierfs2/projects/ImageRegistration/Fiji.app/ImageJ-linux64 -macro /n/schierfs2/projects/ImageRegistration/Fiji.app/scripts/cmdline_lsmStitchAndPrepareCZIsForWarping_cluster.m "sipa1l1_2017_07_26__19_29_00__p$SLURM_ARRAY_TASK_ID.lsm /n/regal/schier_lab/sthyme/microscopyjuly2017/sipa1l1/  486.4"

#source new-modules.sh; module load fastqc
#fastqc --casava -o fastqc_reports A01_R1.pair.fastq.gz
