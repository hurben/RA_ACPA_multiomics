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

kfold_data_dir='../../../analysis/5fold_data_ra_only/network_construction_enet_1condition_p2'
kfold_feature_dir='../../../analysis/post_network_enet_ra_only/5fold/enet_1condition_p2'
folder_name='fs_network_percentage'

rm -r $folder_name
mkdir $folder_name

for split in 1p 5p 10p 20p 25p 30p 40p 50p 100p
do
	echo $split
	for i in 1 2 3 4 5
	do
		echo ${i}
		echo python3 ../../../src/machine_learning/create_feature_selection_matrix.py $kfold_feature_dir/${i}fold.RWR.result.txt $kfold_data_dir/${i}fold $split $folder_name ${i}fold
		python3 ../../../src/machine_learning/create_feature_selection_matrix.py $kfold_feature_dir/${i}fold.RWR.result.txt $kfold_data_dir/${i}fold $split $folder_name ${i}fold
	done
done

