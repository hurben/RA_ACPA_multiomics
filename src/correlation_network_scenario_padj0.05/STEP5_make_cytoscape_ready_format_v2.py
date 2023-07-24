#STEP6_make_cytoscape_ready_format_v2.py         23.02.10

#make cytoscape ready file for Fig. 5

#designed to be runned by make_cytocape_ready_format.sh

#input from: analysis/correlation_network/network_similarity
#output to: analysis/correlation_network/network_similarity


def get_edge_list_of_interest(edge_of_interest_file, edge_list):

	#find rho, pval from sig topology file
	edge_of_interest_open = open(edge_of_interest_file,'r')
	edge_of_interest_readlines = edge_of_interest_open.readlines()

	for i in range(1, len(edge_of_interest_readlines)):
		read = edge_of_interest_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')
		
		target = token[0]
		source = token[1]
		edge_list.append('%s\t%s' % (target, source))

	edge_of_interest_open.close()

	return edge_list

def get_num_readlines(data_file):
	with open(data_file) as f:
		for i, _ in enumerate(f):
			pass
	return i + 1

def fetch_edge_info(edge_list, topology_dict, topology_file, topology_type):

	len_readlines = get_num_readlines(topology_file)
	max_count = len(edge_list)
	count = 0

	with open(topology_file) as topology_open:

		#for readline in topology_open:
		for i in range(len_readlines): #debug purpose
			line = next(topology_open)
			if i != 0: #line 0 is header
				line = line.replace('\n','')
				token = line.split('\t')

				edge_type_a = '%s\t%s' % (token[0], token[1])
				edge_type_b = '%s\t%s' % (token[1], token[0])

				if count < max_count:
					if edge_type_a in edge_list or edge_type_b in edge_list:
						source = token[0]
						target = token[1]
						rho = float(token[2])
						padj = float(token[4])
						topology_dict[source, target, topology_type] = [rho, padj]
						count += 1
				if count == max_count:
					break

	return topology_dict

def write_output(output_txt, source, target, data_dict, condition, index):

	#index 1: print pvalue
	#index 2: print rho
	try:
		value = data_dict[source, target, condition][index]
	except KeyError:
		value = data_dict[target, source, condition][index]
	output_txt.write('\t%s' % value)

if __name__ == "__main__":

	import sys
	import os
	import networkx as networkx

	#get edge from inputfile
	edge_list = []
	pos_rho_edge_file = sys.argv[1]
	neg_rho_edge_file = sys.argv[2]

	edge_list = get_edge_list_of_interest(pos_rho_edge_file, edge_list)
	edge_list = get_edge_list_of_interest(neg_rho_edge_file, edge_list)
	#this will merge inversed relationship between acpa-neg
	#positive correlation in acpa-neg (while negative correlation in acpa-pos)
	#negative correlation in acpa-neg (while positive correlation in acpa-pos)

	output_file = sys.argv[3]

	topology_name_list = ['acpa_neg_3_omics', 'acpa_pos_3_omics', 'control_3_omics']
	
	topology_1_file = '../topology_data_scenario_padj0.05/%s.corr.pad.topology.tsv' % topology_name_list[0]
	topology_2_file = '../topology_data_scenario_padj0.05/%s.corr.pad.topology.tsv' % topology_name_list[1]
	topology_3_file = '../topology_data_scenario_padj0.05/%s.corr.pad.topology.tsv' % topology_name_list[2]

	#find rho, pval from sig topology file
	
	data_dict = {}
	
	data_dict = fetch_edge_info(edge_list, data_dict, topology_1_file, 'acpa_neg')
	data_dict = fetch_edge_info(edge_list, data_dict, topology_2_file, 'acpa_pos')
	data_dict = fetch_edge_info(edge_list, data_dict, topology_3_file, 'control')

	output_txt = open(output_file,'w')
	output_txt.write('source\ttarget\tinfo_type\tpval\trho\tcontrol_pval\tcontrol_rho\n')

	for edge in edge_list:
		source = edge.split('\t')[0]
		target = edge.split('\t')[1]

		#write acpa-neg info first
		condition = 'acpa_neg'
		output_txt.write('%s\t%s\t%s' % (source,target,condition))

		write_output(output_txt, source, target, data_dict, condition, 1) #pval
		write_output(output_txt, source, target, data_dict, condition, 0) #rho
		write_output(output_txt, source, target, data_dict, 'control', 1) #pval
		write_output(output_txt, source, target, data_dict, 'control', 0) #rho
		output_txt.write('\n')

		#write acpa-pos 
		condition = 'acpa_pos'
		output_txt.write('%s\t%s\t%s' % (target, source,condition)) #writing target, source awkwards for visualization purpose

		write_output(output_txt, source, target, data_dict, condition, 1) #pval
		write_output(output_txt, source, target, data_dict, condition, 0) #rho
		write_output(output_txt, source, target, data_dict, 'control', 1) #pval
		write_output(output_txt, source, target, data_dict, 'control', 0) #rho
		output_txt.write('\n')

	output_txt.close()

