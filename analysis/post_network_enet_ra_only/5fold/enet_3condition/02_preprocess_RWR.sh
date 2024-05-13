for i in 1 2 3 4 5
do
	python3 ../../../../src/post_network/cleanup_RWR_ready_file.py ${i}fold.topology.tsv ${i}fold.topology.v2.tsv
done
