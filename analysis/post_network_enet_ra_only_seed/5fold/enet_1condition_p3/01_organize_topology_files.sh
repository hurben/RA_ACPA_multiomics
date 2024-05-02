#!/bin/bash
#SBATCH --job-name=c1p3_enet_5fold_batch1
#SBATCH --partition=cpu-short
#$BATCH -n 16
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=4
#SBATCH --output test.stdout
#SBATCH --error test.stderr
#SBATCH --mail-user=hur.benjamin@mayo.edu
#SBATCH --mail-type=END
#SBATCH --time=72:00:00
#SBATCH --mem=32G
#$SBATCH --signal=USR1@60

kfold_dir=../../../../analysis/5fold_data_ra_only_seed/network_construction_enet_1condition_p3/result/
multiplex_file_name=multiplex.enet.tsv

for i in 1 2 3 4 5
do
	echo ${i}fold
	python3 ../../../../src/post_network/integrate_network.v2.py $kfold_dir/${i}fold $multiplex_file_name ${i}fold.topology.tsv
done

#test run
#echo python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test
#nohup python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test &
