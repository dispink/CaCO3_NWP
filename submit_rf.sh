#!/usr/bin/env bash

#SBATCH -J grid_rf
#SBATCH --qos normal
#SBATCH --output=/home/users/aslee/CaCO3_NWP/job_logs/slurm-%j.txt
#SBATCH -c 64
#SBATCH --mem=240GB
#SBATCH -t 24:00:00


#/home/users/aslee/miniconda3/bin/python /home/users/aslee/CaCO3_NWP/grid_toc_rf.py
/home/users/aslee/miniconda3/envs/caco3/bin/python /home/users/aslee/CaCO3_NWP/grid_rf.py CaCO3%
