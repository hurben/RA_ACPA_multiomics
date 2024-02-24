seed_list=../seed_of_interest.list

python3 ../../../src/post_network/RWR_create_seed_profile.py full_data.topology.v2.tsv $seed_list full_data.p0.txt

#test run
#echo python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test
#nohup python3 ../../src/post_network/integrate_network.py $kfold_dir $data_index test &
