#!/bin/bash
#$ -cwd
#$ -N c3_enet_5fold_batch1
#$ -q 7-day
#$ -pe threaded 1
#$ -j y
#$ -M hur.benjamin@mayo.edu
#$ -m ae
#$ -l h_vmem=16G
#$ -l h_stack=20M
#$ -V

python3 ../../../src/network_construction_5fold/enet_construction_batch1.py
