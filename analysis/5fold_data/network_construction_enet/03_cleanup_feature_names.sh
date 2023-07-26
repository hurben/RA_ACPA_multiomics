folder_name=result

for i in 1 2 3 4 5 6 7 8 9 10
do
	echo python ../../../src/network_construction_10fold/network_output_cleanup.py $folder_name/${i}fold/multiplex.enet.tsv
	python ../../../src/network_construction_10fold/network_output_cleanup.py $folder_name/${i}fold/multiplex.enet.tsv
done
