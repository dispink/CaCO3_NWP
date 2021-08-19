#!/usr/bin/env bash

#SBATCH -J grid_svr
#SBATCH --qos normal
#SBATCH --output=/home/users/aslee/CaCO3_NWP/job_logs/slurm-%j.txt
#SBATCH -c 64
#SBATCH --mem=200GB
#SBATCH -t 24:00:00


#/home/users/aslee/miniconda3/bin/python /home/users/aslee/CaCO3_NWP/grid_toc.py
#/home/users/aslee/miniconda3/bin/python /home/users/aslee/CaCO3_NWP/grid_caco3.py
/home/users/aslee/miniconda3/envs/caco3/bin/python /home/users/aslee/CaCO3_NWP/grid_svr.py
