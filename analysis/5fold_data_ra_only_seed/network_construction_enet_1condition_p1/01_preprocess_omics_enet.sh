for i in 1 2 3 4 5
do
	folder=${i}fold
	rm -r $folder
done
python3 ../../../src/acpa_specific_network_construction_5fold/enet_construction_preprocess_1condition_p1.py
