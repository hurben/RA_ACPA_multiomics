#!/bin/bash
#$ -cwd
#$ -N fs_5fold_3c
#$ -q 7-day
#$ -pe threaded 1
#$ -j y
#$ -M hur.benjamin@mayo.edu
#$ -m ae
#$ -l h_vmem=30G
#$ -V

kfold_data_dir='../../../../analysis/5fold_data/network_construction_enet'
kfold_feature_dir='../../../../analysis/post_network_enet/5fold/enet_3condition'
folder_name='fs_network_topn'

rm -r $folder_name
mkdir $folder_name

for split in 10 20 30 40 50 60 70 80 90 100 200 300 400 500 600 700 800 900 1000
do
	echo $split
	for i in 1 2 3 4 5
	do
		echo ${i}
		echo python3 ../../../../src/machine_learning/create_feature_selection_matrix.py $kfold_feature_dir/${i}fold.RWR.result.txt $kfold_data_dir/${i}fold top$split $folder_name ${i}fold
		python3 ../../../../src/machine_learning/create_feature_selection_matrix.py $kfold_feature_dir/${i}fold.RWR.result.txt $kfold_data_dir/${i}fold top$split $folder_name ${i}fold
	done
done
