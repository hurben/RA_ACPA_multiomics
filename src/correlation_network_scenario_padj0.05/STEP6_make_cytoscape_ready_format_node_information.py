#STEP6_make_cytoscape_ready_format_node_information.py

#make cytoscape ready file for Fig. 5
#designed to be run after make_cytocape_ready_format.sh

#mainly get node information to tweak around cytoscape

#aa = autoantibody
#p_ = protein
#m_ = metabolites


if __name__ == "__main__":

	import sys
	import os
	import networkx as networkx
	import pandas as pd

	input_file = sys.argv[1]
	output_file = sys.argv[2]

	input_df = pd.read_csv(input_file, sep = "\t") 
	r, c = input_df.shape

	node_list = []

	for i in range(r):
		source = input_df["source"][i]
		target = input_df["target"][i]

		node_list.append(source)
		node_list.append(target)

	node_list = list(set(node_list))

	output_txt = open(output_file,'w')
	output_txt.write("node\tnode_type\n")
	for node in node_list:
		node_type = 0
		if "p_" in node:
			node_type = 1
		if "aa_" in node:
			node_type = 2
		output_txt.write("%s\t%s\n" % (node, node_type))

	output_txt.close()




