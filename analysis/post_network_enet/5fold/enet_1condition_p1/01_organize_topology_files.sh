#!/bin/bash
#$ -cwd
#$ -N enet_1condition_p1
#$ -q 7-day
#$ -pe threaded 1
#$ -j y
#$ -M hur.benjamin@mayo.edu
#$ -m ae
#$ -l h_vmem=16G
#$ -V

kfold_dir=../../../../analysis/5fold_data/network_construction_enet_1condition_p1/result/
multiplex_file_name=multiplex.enet.tsv

for i in 1 2 3 4 5
do
	echo ${i}fold
	python3 ../../../../src/post_network/integrate_network.v2.py $kfold_dir/${i}fold $multiplex_file_name ${i}fold.topology.tsv
done

#test run
#echo python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test
#nohup python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test &
