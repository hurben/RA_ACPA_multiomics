#"find_subnetwork_from_cyto_file.py" 22.01.22
#
#designed to make a subnetwork file from cytoscape ready file from full_data.topology.tsv (which is an adjacancy matrix)
#output is a text file with two columns, 
#source\ttarget\n
#
#IMPORTANT NOTE: the input file should have same number of rows and columns

def make_dict_from_rwr_result_file(input_file, cutoff):

	temp_dict = {}
	input_df = pd.read_csv(input_file, sep="\t", header=None)

	rank_count = 0
	count_value = 0
	for i in range(int(cutoff)+ 1):
		feature = input_df.iloc[i][0]
		value = round((input_df.iloc[i][1]), 5) 

		if value != count_value:
			temp_dict[feature] = rank_count + 1
			count_value = value
			rank_count = rank_count + 1

		if value == count_value:
			temp_dict[feature] = rank_count

	return temp_dict

if __name__ == '__main__':

	import sys
	import pandas as pd

	input_file = sys.argv[1]
	rwr_result_file = sys.argv[2]
	defined_rwr_cutoff = sys.argv[3]
	output_file = sys.argv[4]
	output_profile_file = sys.argv[5]

	rwr_ranked_node_dict = make_dict_from_rwr_result_file(rwr_result_file, defined_rwr_cutoff)

	input_df = pd.read_csv(input_file, sep="\t")
	r, c = input_df.shape
	
	rwr_node_list = list(rwr_ranked_node_dict.keys())

	output_txt = open(output_file,'w')
	output_txt.write('source\ttarget\n')
	for i in range(r):

		step = i % 10000
		if step == 0:
			print ("%s/%s" % (i,r))

		source = input_df.iloc[i][0]
		target = input_df.iloc[i][1]
		if source in rwr_node_list and target in rwr_node_list:
			output_txt.write('%s\t%s\n' % (source, target))
	output_txt.close()

	output_txt = open(output_profile_file,'w')
	output_txt.write('node\trank\n')
	for node in list(rwr_ranked_node_dict.keys()):
		rank = rwr_ranked_node_dict[node]
		output_txt.write('%s\t%s\n' % (node, rank))
	output_txt.close()
