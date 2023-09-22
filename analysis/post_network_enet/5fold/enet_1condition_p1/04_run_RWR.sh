for i in 1 2 3 4 5
do
	Rscript ../../../../src/post_network/RWR.R ${i}fold.topology.v2.tsv ${i}fold.p0.txt ${i}fold.RWR.result.txt
done
