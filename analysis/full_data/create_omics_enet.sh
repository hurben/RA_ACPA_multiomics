#!/bin/bash
#$ -cwd
#$ -N rwr_enet_full
#$ -q 7-day
#$ -pe threaded 1
#$ -j y
#$ -M hur.benjamin@mayo.edu
#$ -m ae
#$ -l h_vmem=32G
#$ -V

Rscript ../../src/network_construction_5fold/ElasticNet_R.short.fulldata.r three_omics_multiplex.tsv three_omics_multiplex.enet.tsv
