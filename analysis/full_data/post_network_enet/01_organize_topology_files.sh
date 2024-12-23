#!/bin/bash
#$ -cwd
#$ -N enet_full
#$ -q 7-day
#$ -pe threaded 1
#$ -j y
#$ -M hur.benjamin@mayo.edu
#$ -m ae
#$ -l h_vmem=32G
#$ -V

data_dir=../../../analysis/full_data
multiplex_file_name=two_omics_multiplex.enet.tsv

python3 ../../../src/post_network/integrate_network.v2.py $data_dir $multiplex_file_name full_data.topology.tsv
