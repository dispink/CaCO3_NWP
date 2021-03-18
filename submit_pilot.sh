#!/usr/bin/env bash

#SBATCH -J grid_pilot
#SBATCH --qos normal
#SBATCH --output=/home/users/aslee/CaCO3_NWP/job_logs/slurm-%j.txt
#SBATCH --hint=multithread
#SBATCH --nodes=1 --exclusive --cpus-per-task=1 --ntasks-per-node=64
#SBATCH --mem=240GB
#SBATCH -t 1:00:00


/home/users/aslee/miniconda3/bin/python /home/users/aslee/CaCO3_NWP/grid_pilot_ridge.py
#/home/users/aslee/miniconda3/bin/python /home/users/aslee/CaCO3_NWP/grid_pilot_svr.py
