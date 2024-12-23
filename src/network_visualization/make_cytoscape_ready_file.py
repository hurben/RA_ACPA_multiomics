#"make_cytoscape_ready_file.py"     22.01.22
#
#designed to make a cytoscape ready file from full_data.topology.tsv (which is an adjacancy matrix)
#output is a text file with two columns, 
#source\ttarget\n
#
#IMPORTANT NOTE: the input file should have same number of rows and columns

if __name__ == '__main__':

	import sys
	import pandas as pd
	import networkx as nx

	input_file = sys.argv[1]
	output_file = sys.argv[2]

	input_df = pd.read_csv(input_file, sep="\t", index_col = 0)
	r, c = input_df.shape

	x_axis_feature_list = input_df.columns.values
	y_axis_feature_list = input_df.index.values

	G = nx.Graph()
	
	#Make graph from data_df
	for i in range(r):
		feature_source = x_axis_feature_list[i]
		for j in range(c):
			feature_target = y_axis_feature_list[j]
			value = input_df.iloc[i][j]
			if value > 0:
				G.add_edge(feature_source, feature_target)

	#this will naturally remove duplicate edges
	print ("Number of total nodes: %s", len(G.nodes))
	print ("Number of total edges: %s", len(G.edges))

	edge_list = list(G.edges)

	#Make output
	output_txt = open(output_file,'w')
	output_txt.write('source\ttarget\n')
	for i in range(len(edge_list)):
		source = edge_list[i][0]
		target = edge_list[i][1]
		output_txt.write('%s\t%s\n' % (source, target))
	output_txt.close()
