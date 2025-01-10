#!/bin/bash
#SBATCH --job-name=c3_enet_5fold_batch1
#SBATCH --partition=cpu-short
#$BATCH -n 16
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=4
#SBATCH --output test.stdout
#SBATCH --error test.stderr
#SBATCH --mail-user=hur.benjamin@mayo.edu
#SBATCH --mail-type=END
#SBATCH --time=72:00:00
#SBATCH --mem=32G
#$SBATCH --signal=USR1@60

input="$1"

python3 ../../../src/network_construction_5fold_ra_only/enet_construction_batch1.py $input
