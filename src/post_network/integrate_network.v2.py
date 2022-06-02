#"integrate_network.py"
#
#From the infered network (calculated by ElasticNet), we will obtain matrix of coefficients.
#We will now infer an adjacency matrix from this file.
#Note
# [0] Coefficients will be considered as edges, while fully penalized variables (coefficeint = 0) will consider to have no edges
# [1] If two nodes share edges at least one time, this will consider as edge.
#     ex1) node A - node B
#     ex2) node B   node A
#     node A and node B will have edge.
# [2] We are removing duplicated edges
# [3] We are not considering "causality"
# [4] Every edge has the same weight.
#
#Intended input: output from "ElasticNet_R.short.r" which is "result/multiplex.enet.tsv"

if __name__ == "__main__":

	import pandas as pd
	import numpy as np
	import networkx as nx
	import sys
	import os
	import scipy as sp

	topology_folder_dir = sys.argv[1]	#either kfold or other folder
	topology_name = sys.argv[2]
	output_file = sys.argv[3] 			#summarized topology

	topology_dict = {}

	G = nx.Graph()

	#read topology file,
	topology_file = '%s/%s' % (topology_folder_dir, topology_name)
	topology_df = pd.read_csv(topology_file, sep='\t', index_col=0)

	row_list = topology_df.index.values
	col_list = topology_df.columns.values
	r, c = topology_df.shape
	
	#create graph from each topology file
	for i in range(r):
		row_name = row_list[i] #infered as source node
		for j in range(c):
			col_name = col_list[j] #infered as target node
			value = topology_df.iloc[i][j]  #this is coefficient calculated by ElasticNet. We will uses this to infer the weight of the edge (although this will be imputed 1 or 0)
			if value > 0 or value < 0:
				G.add_edge(row_name, col_name)

	#summarize node_list, edge_list
	node_list = G.nodes
	edge_list = G.edges

	adj_dict = {}
	#initialize the adjacency dict
	for source in node_list:
		for target in node_list:
			adj_dict[source, target] = 0

	#Fill up the adjacency dict
	for edge in edge_list:
		source = edge[0]
		target = edge[1]
		adj_dict[source, target] = 1
		adj_dict[target, source] = 1

	#create integrated adj text
	output_txt = open(output_file,'w')
	for node in node_list:
		output_txt.write('\t%s' % node)
	output_txt.write('\n')

	for source in node_list:
		output_txt.write(source)
		for target in node_list:
			value = adj_dict[source, target]
			output_txt.write('\t%s' % value)
		output_txt.write('\n')
	output_txt.close()

	print (topology_folder_dir)
	print ("# Edges: ",len(edge_list))
	print ("# Nodes: ",len(node_list))

else:
	None

