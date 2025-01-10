for i in 1 2 3 4 5
do
	folder=${i}fold
	rm -r $folder
done
python3 ../../../src/network_construction_5fold_ra_only/enet_construction_preprocess.py
