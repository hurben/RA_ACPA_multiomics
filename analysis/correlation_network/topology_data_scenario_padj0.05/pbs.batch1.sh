#!/bin/bash
#$ -cwd
#$ -N control_corr
#$ -q 1-day
#$ -pe threaded 8
#$ -j y
#$ -m ae
#$ -l h_vmem=8G
#$ -V
#$ -shell y

python3 ../../src/correlation_network/STEP1_make_sigNcorr_results_v2.py control_3_omics
