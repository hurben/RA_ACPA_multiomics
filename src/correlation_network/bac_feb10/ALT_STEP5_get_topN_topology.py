#ALT_STEP5_get_topN_topology.py" 22.12.19
#

def get_topN_edges(topology_file, rho_direction, topN):

	data_dict = {}
	node_list = []
	topology_df = pd.read_csv(topology_file, sep="\t")

	if rho_direction == "pos":
		topology_df = topology_df.sort_values("rho", ascending=False)
	if rho_direction == "neg":
		topology_df = topology_df.sort_values("rho", ascending=True)

	for i in range(topN):
		source = topology_df["source"][i]
		target = topology_df["target"][i]
		rho = topology_df["rho"][i]
		padj = topology_df["pad"][i]

		data_dict[source,target] = [rho, padj]
		node_list.append(source)
		node_list.append(target)

	node_list = list(set(node_list))

	return data_dict, node_list

def get_deg_dict(node_list):

	diff_dir = '../../../analysis/statistics/linear_model/differential_abundance'
	omics_list = ['autoantibody','metabolomics','proteomics']
	comparison_list = ['cVSneg','cVSpos','negVSpos','cVSra']
	# comparison_list = ['cVSneg','cVSpos']

	deg_dict = {}

	for omics_type in omics_list:
		for comparison_type in comparison_list:
			deg_file = "%s/%s.%s.padj.v2.tsv" % (diff_dir, omics_type, comparison_type)
			deg_df = pd.read_csv(deg_file,sep="\t")
			r, c = deg_df.shape
			for i in range(r):
				feature_name = deg_df.iloc[i][0]
				pval = deg_df.iloc[i][3]
				fc = deg_df.iloc[i][2]

				if omics_type == "autoantibody":
					feature_name = "aa_%s" % feature_name
				if omics_type == "proteomics":
					feature_name = "p_%s" % feature_name

				if feature_name in node_list:
					deg_dict[feature_name, comparison_type] = [pval, fc]

	return deg_dict

def write_output(data_dict, node_list, output_name, rho_direction, topN):

	output_file = '%s.%s.top%s.topology.tsv' % (output_name, rho_direction, topN)
	output_txt = open(output_file,'w')
	output_txt.write('source\ttarget\trho\tpadj\n')
	for edge in list(data_dict.keys()):
		source = edge[0]
		target = edge[1]
		rho = data_dict[edge][0]
		padj = data_dict[edge][1]

		output_txt.write('%s\t%s' % (source, target))
		output_txt.write('\t%s\t%s\n' % (rho, padj))
	output_txt.close()

	deg_dict = get_deg_dict(node_list)
	comparison_list = ['cVSneg','cVSpos','negVSpos','cVSra']

	output_file = '%s.%s.top%s.profile.tsv' % (output_name, rho_direction, topN)
	output_txt = open(output_file,'w')

	output_txt.write('feature')
	for comparison_type in comparison_list:
		output_txt.write('\t%s_pval\t%s_log2fc' % (comparison_type, comparison_type))
	output_txt.write('\n')
	
	for node in node_list:
		output_txt.write('%s' % node)

		for comparison_type in comparison_list:
			try: 
				padj = deg_dict[node, comparison_type][0]
			except KeyError:
				padj = 'nan'
			try: 
				log2fc = deg_dict[node, comparison_type][1]
			except KeyError:
				log2fc = 'nan'
			
			output_txt.write('\t%s\t%s' % (padj, log2fc))

		output_txt.write('\n')

if __name__ == "__main__":

	import sys
	import pandas as pd

	#load network_topologys (six in total)
	topology_1_name = sys.argv[1] 
	topology_2_name = sys.argv[2] 
	topology_3_name = sys.argv[3] 

	topology_1_pos_file = '../topology_data/%s.corr.pad.sig.pos.topology.tsv' % topology_1_name
	topology_2_pos_file = '../topology_data/%s.corr.pad.sig.pos.topology.tsv' % topology_2_name
	topology_3_pos_file = '../topology_data/%s.corr.pad.sig.pos.topology.tsv' % topology_3_name
	
	topology_1_neg_file = '../topology_data/%s.corr.pad.sig.neg.topology.tsv' % topology_1_name
	topology_2_neg_file = '../topology_data/%s.corr.pad.sig.neg.topology.tsv' % topology_2_name
	topology_3_neg_file = '../topology_data/%s.corr.pad.sig.neg.topology.tsv' % topology_3_name

	#get edge list
	topN = 100
	topology_1_pos_dict, topology_1_pos_node_list = get_topN_edges(topology_1_pos_file, 'pos', topN)
	topology_2_pos_dict, topology_2_pos_node_list = get_topN_edges(topology_2_pos_file, 'pos', topN)
	topology_3_pos_dict, topology_3_pos_node_list = get_topN_edges(topology_3_pos_file, 'pos', topN)

	topology_1_neg_dict, topology_1_neg_node_list = get_topN_edges(topology_1_neg_file, 'neg', topN)
	topology_2_neg_dict, topology_2_neg_node_list = get_topN_edges(topology_2_neg_file, 'neg', topN)
	topology_3_neg_dict, topology_3_neg_node_list = get_topN_edges(topology_3_neg_file, 'neg', topN)

	#[1]make topology/profile file of top 100 edges (RHO, PADJ)
	#[2]also make node information list (DEG, PADJ, LOG2FC)
	write_output(topology_1_pos_dict, topology_1_pos_node_list, 'acpa_neg', 'pos', topN)
	write_output(topology_2_pos_dict, topology_2_pos_node_list, 'acpa_pos', 'pos', topN)
	write_output(topology_3_pos_dict, topology_3_pos_node_list, 'control', 'pos', topN)

	write_output(topology_1_neg_dict, topology_1_neg_node_list, 'acpa_neg', 'neg', topN)
	write_output(topology_2_neg_dict, topology_2_neg_node_list, 'acpa_pos', 'neg', topN)
	write_output(topology_3_neg_dict, topology_3_neg_node_list, 'control', 'neg', topN)


	
	#[1]make node info matrix (ACPAneg pos, ACPAneg pos, ACPApos neg, ACPApos pos, Control neg, Control pos)
	#value is 0 or 1 (exisiting in node list)

