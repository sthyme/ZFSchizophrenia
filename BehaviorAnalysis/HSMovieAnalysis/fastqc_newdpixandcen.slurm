#!/bin/bash

#SBATCH -p serial_requeue # Partition to submit to

#SBATCH -n 1 # Number of cores requested
#SBATCH --exclusive
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-socket=1
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 30 # Runtime in minutes
#SBATCH --mem=16000 # Memory per cpu in MB (see also --mem-per-cpu)
#SBATCH --job-name=arrayJob
#SBATCH --array=817,602,62
#SBATCH -o hostname_%A_%a.out # Standard out goes to this file
#SBATCH -e hostname_%A_%a.err # Standard err goes to this filehostname

module load opencv/3.0.0-fasrc04
xvfb-run -a python /n/schierfs2/projects/ImageRegistration/behaviorscripts/FinalPyTracker_movedfromregal/highspeedmovieanalysis.py -c "testlog.centroid1.Fri, Aug 25, 2017" -m "hsmovieFri, Aug 25, 2017_$SLURM_ARRAY_TASK_ID.avi"

#source new-modules.sh; module load fastqc
#fastqc --casava -o fastqc_reports A01_R1.pair.fastq.gz
