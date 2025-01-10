#!/bin/bash

#for ((i=0; i<= 1; i++))
for ((i=0; i<= 500; i++))
do
	echo $i
	seed_directory=seed_$i
	if [ -d "$seed_directory" ]; then
		rm -r "$seed_directory"
		mkdir "$seed_directory"
		mkdir "$seed_directory/enet_1condition_p1"
		mkdir "$seed_directory/enet_1condition_p3"
		mkdir "$seed_directory/enet_2condition"
	else
		mkdir "$seed_directory"
		mkdir "$seed_directory/enet_1condition_p1"
		mkdir "$seed_directory/enet_1condition_p3"
		mkdir "$seed_directory/enet_2condition"
	fi

	#top
	#control vs ra
	python3 ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_topn_cVSra top $seed_directory/enet_1condition_p1/classification.topN.result.cVSra.enet.tsv control_ra $i
	python3 ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_topn_cVSra top $seed_directory/enet_1condition_p3/classification.topN.result.cVSra.enet.tsv control_ra $i
	python3 ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_2condition/fs_network_topn_cVSra top $seed_directory/enet_2condition/classification.topN.result.cVSra.enet.tsv control_ra $i

	#p1
	#control vs pos
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_topn_cVSpos top $seed_directory/enet_1condition_p1/classification.topN.result.cVSpos.enet.tsv control_pos $i
	#control vs neg
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_topn_cVSneg top $seed_directory/enet_1condition_p1/classification.topN.result.cVSneg.enet.tsv control_neg $i

	#p3
	#control vs pos
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_topn_cVSpos top $seed_directory/enet_1condition_p3/classification.topN.result.cVSpos.enet.tsv control_pos $i
	#control vs neg
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_topn_cVSneg top $seed_directory/enet_1condition_p3/classification.topN.result.cVSneg.enet.tsv control_neg $i

	#multi-omics
	#control vs pos
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_2condition/fs_network_topn_cVSpos top $seed_directory/enet_2condition/classification.topN.result.cVSpos.enet.tsv control_pos $i
	#control vs neg
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_2condition/fs_network_topn_cVSneg top $seed_directory/enet_2condition/classification.topN.result.cVSneg.enet.tsv control_neg $i

	#Percentage
	#control vs ra
	python3 ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_percentage_cVSra percentage $seed_directory/enet_1condition_p1/classification.result.cVSra.enet.tsv control_ra $i
	python3 ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_percentage_cVSra percentage $seed_directory/enet_1condition_p3/classification.result.cVSra.enet.tsv control_ra $i
	python3 ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_2condition/fs_network_percentage_cVSra percentage $seed_directory/enet_2condition/classification.result.cVSra.enet.tsv control_ra $i

	#p1
	#control vs pos
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_percentage_cVSpos percentage $seed_directory/enet_1condition_p1/classification.result.cVSpos.enet.tsv control_pos $i
	#control vs neg
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p1/fs_network_percentage_cVSneg percentage $seed_directory/enet_1condition_p1/classification.result.cVSneg.enet.tsv control_neg $i

	#p3
	#control vs pos
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_percentage_cVSpos percentage $seed_directory/enet_1condition_p3/classification.result.cVSpos.enet.tsv control_pos $i
	#control vs neg
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_1condition_p3/fs_network_percentage_cVSneg percentage $seed_directory/enet_1condition_p3/classification.result.cVSneg.enet.tsv control_neg $i

	#multi-omics
	#control vs pos
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_2condition/fs_network_percentage_cVSpos percentage $seed_directory/enet_2condition/classification.result.cVSpos.enet.tsv control_pos $i
	#control vs neg
	python3  ../../../src/machine_learning/classification_5fold.2class.opti.withMCC.py enet_2condition/fs_network_percentage_cVSneg percentage $seed_directory/enet_2condition/classification.result.cVSneg.enet.tsv control_neg $i

	python3 ../../../src/machine_learning/summarize_ML_results.opti.py $seed_directory/ml_summary.tsv $seed_directory

done
