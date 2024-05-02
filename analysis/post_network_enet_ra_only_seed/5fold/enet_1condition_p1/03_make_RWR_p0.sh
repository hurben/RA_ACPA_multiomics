seed_list=../seed_of_interest.list

for i in 1 2 3 4 5
do
	adj_matrix=${i}fold.topology.v2.tsv
	echo python3 ../../../../src/post_network/RWR_create_seed_profile.py $adj_matrix $seed_list ${i}fold.p0.txt
	python3 ../../../../src/post_network/RWR_create_seed_profile.py $adj_matrix $seed_list ${i}fold.p0.txt
done

#test run
#echo python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test
#nohup python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test &
