for i in 1 2 3 4 5
do
	folder=${i}fold
	rm -r $folder
done
python3 ../../../src/network_construction_5fold/enet_construction_preprocess_1condition_p3.py
