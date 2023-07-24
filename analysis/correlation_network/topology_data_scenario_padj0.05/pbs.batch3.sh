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

python3 ../../src/correlation_network/STEP2_make_sigNcorr_results_v2.py acpa_pos_3_omics
