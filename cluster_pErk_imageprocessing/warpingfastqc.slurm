#!/bin/bash

#SBATCH -p serial_requeue # Partition to submit to

#SBATCH -n 1 # Number of cores requested
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 200 # Runtime in minutes
#SBATCH --mem=4000 # Memory per cpu in MB (see also --mem-per-cpu)
#SBATCH --job-name=arrayJob
#SBATCH --array=1-35
#SBATCH -o hostname_%A_%a.out # Standard out goes to this file
#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname

#echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

/n/schierfs1/projects/ImageRegistration/cmtk-3.2.3/build/bin/reformatx -o /n/schier_lab2/users/sthyme/ppimicrosopyandlastfew/augustmicroscopy/znf536hetinx/reformatted.$SLURM_ARRAY_TASK_ID/jacobian_$SLURM_ARRAY_TASK_ID.nrrd /n/schierfs1/projects/ImageRegistration/data/Ref20131120pt14pl2.nrrd --jacobian /n/schier_lab2/users/sthyme/ppimicrosopyandlastfew/augustmicroscopy/znf536hetinx/Registration.$SLURM_ARRAY_TASK_ID/warp/$SLURM_ARRAY_TASK_ID/*/registration

#source new-modules.sh; module load fastqc
#fastqc --casava -o fastqc_reports A01_R1.pair.fastq.gz
