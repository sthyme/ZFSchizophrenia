#!/bin/bash

#SBATCH -p serial_requeue # Partition to submit to

#SBATCH -n 32 # Number of cores requested
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 200 # Runtime in minutes
#SBATCH --mem=4000 # Memory per cpu in MB (see also --mem-per-cpu)
#SBATCH --job-name=arrayJob
#SBATCH --array=1-60
#SBATCH -o hostname_%A_%a.out # Standard out goes to this file
#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname

/n/schierfs2/projects/ImageRegistration/cmtk-3.2.3/build/bin/munger -b /n/schierfs2/projects/ImageRegistration/cmtk-3.2.3/build/bin/ -T 32 -awr 010203 -X 52 -G 80 -R 3 -A '--accuracy 0.8' -W '--accuracy 1.6' -s /n/schierfs2/projects/ImageRegistration/data/Ref20131120pt14pl2.nrrd -d .$SLURM_ARRAY_TASK_ID -v images/$SLURM_ARRAY_TASK_ID/

#source new-modules.sh; module load fastqc
#fastqc --casava -o fastqc_reports A01_R1.pair.fastq.gz
