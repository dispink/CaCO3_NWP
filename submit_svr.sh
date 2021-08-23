#!/usr/bin/env bash

#SBATCH -J grid_svr
#SBATCH --qos normal
#SBATCH --output=/home/users/aslee/CaCO3_NWP/job_logs/slurm-%j.txt
#SBATCH -c 64
#SBATCH --mem=50GB
#SBATCH -t 20:00:00


#/home/users/aslee/miniconda3/bin/python /home/users/aslee/CaCO3_NWP/grid_toc.py
#/home/users/aslee/miniconda3/bin/python /home/users/aslee/CaCO3_NWP/grid_caco3.py
/home/users/aslee/miniconda3/envs/caco3/bin/python /home/users/aslee/CaCO3_NWP/grid_svr.py CaCO3% 2-1
