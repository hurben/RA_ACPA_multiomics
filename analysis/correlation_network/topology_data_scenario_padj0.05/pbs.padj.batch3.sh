#!/bin/bash
#$ -cwd
#$ -N acpa_pos_corr
#$ -q 1-day
#$ -pe threaded 8
#$ -j y
#$ -m ae
#$ -l h_vmem=8G
#$ -V
#$ -shell y

python3 ../../src/correlation_network/STEP3_update_topology_pad.py acpa_pos_3_omics
