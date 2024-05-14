#!/bin/bash
#SBATCH --job-name=Test2
#SBATCH --partition=cpu-short
#$BATCH -n 16
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=4
#SBATCH --output test.stdout
#SBATCH --error test.stderr
#SBATCH --mail-user=hur.benjamin@mayo.edu
#SBATCH --mail-type=END
#SBATCH --time=72:00:00
#SBATCH --mem=64G
#$SBATCH --signal=USR1@60

data_dir=../../../analysis/full_data_metabolomics_neg_pos
multiplex_file_name=metabolomics_ML_ready.v2.enet.tsv

python3 ../../../src/post_network/integrate_network.v2.py $data_dir $multiplex_file_name metabolomics_full_data.topology.tsv
