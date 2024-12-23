#!/bin/bash
#SBATCH --job-name=c1_enet_5fold_batch1
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

Rscript ../../src/network_construction_5fold/ElasticNet_R.short.fulldata.r ../../preprocessed_data/2_omics/two_omics_multiplex.tsv two_omics_multiplex.enet.tsv
