#RWR_create_seed_profile.py           21.07.12
#
#create p0 list from the adjacency matrix (results from: integrate_network.py)

#Intended input [1]: output from "cleanup_RWR_ready_file.py"; which is Kfold.topology.v2.tsv
#Intended input [2]: a text file made by me; which is "seed_of_interest.list"

if __name__ == "__main__":

	import pandas as pd
	import sys

	adj_matrix_file = sys.argv[1]
	seed_of_interest_file = sys.argv[2]
	output_file = sys.argv[3]

	#create node list
	adj_pd = pd.read_csv(adj_matrix_file, sep='\t', index_col=0)
	node_list = adj_pd.index.values

	#get seed list
	seed_list = []
	seed_of_interest_open = open(seed_of_interest_file,'r')
	seed_of_interest_readlines = seed_of_interest_open.readlines()

	for i in range(len(seed_of_interest_readlines)):
		read = seed_of_interest_readlines[i]
		read = read.replace('\n','')
		seed_list.append(read)

	#create p0 file
	print (output_file)
	output_txt = open(output_file,'w')
	for node in node_list:
		seed = 0
		if node in seed_list:
			seed = 1
		output_txt.write('%s\t%s\n' % (node,seed))
	output_txt.close()

