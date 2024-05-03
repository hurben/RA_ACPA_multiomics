#!/bin/bash

#for i in "${numbers[@]}"
for ((i=0; i<= 200; i++))
#for i in 118 87 20 182
do
	echo $i
	seed_directory=seed_$i
	if [ -d "$seed_directory" ]; then
		rm -r "$seed_directory"
		mkdir "$seed_directory"
		mkdir "$seed_directory/enet_1condition_p1"
		mkdir "$seed_directory/enet_1condition_p2"
		mkdir "$seed_directory/enet_1condition_p3"
		mkdir "$seed_directory/enet_3condition"
	else
		mkdir "$seed_directory"
		mkdir "$seed_directory/enet_1condition_p1"
		mkdir "$seed_directory/enet_1condition_p2"
		mkdir "$seed_directory/enet_1condition_p3"
		mkdir "$seed_directory/enet_3condition"
	fi

	#top
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_topn_posVSneg top $seed_directory/enet_1condition_p1/classification.topN.result.posVSneg.enet.tsv pos_neg $i
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p2/fs_network_topn_posVSneg top $seed_directory/enet_1condition_p2/classification.topN.result.posVSneg.enet.tsv pos_neg $i
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_topn_posVSneg top $seed_directory/enet_1condition_p3/classification.topN.result.posVSneg.enet.tsv pos_neg $i
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_3condition/fs_network_topn_posVSneg top $seed_directory/enet_3condition/classification.topN.result.posVSneg.enet.tsv pos_neg $i

	#percent
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_percentage_posVSneg percentage $seed_directory/enet_1condition_p1/classification.result.posVSneg.enet.tsv pos_neg $i
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p2/fs_network_percentage_posVSneg percentage $seed_directory/enet_1condition_p2/classification.result.posVSneg.enet.tsv pos_neg $i
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_percentage_posVSneg percentage $seed_directory/enet_1condition_p3/classification.result.posVSneg.enet.tsv pos_neg $i
	python3 ../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_3condition/fs_network_percentage_posVSneg percentage $seed_directory/enet_3condition/classification.result.posVSneg.enet.tsv pos_neg $i

	python3 ../../src/machine_learning/summarize_ML_results.opti.posVSneg.py $seed_directory/ml_summary.tsv $seed_directory
done
