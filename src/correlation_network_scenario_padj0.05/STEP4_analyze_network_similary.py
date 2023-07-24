#STEP5_analyze_network_similary.py   12.05.04
#
#Playing around with the network topology (correlation network, defined by adjusted P-value and Rho)
#Objective: Find common edges, unique edges

#input from: analysis/correlation_network/topology_data
#output stored: analysis/correlation_network/network_similarity

#designed to be runned by: network_similarity.sh


def init_topolgy_graph(data_file):

	data_graph = nx.Graph() #initial lize empty graph

	with open(data_file) as open_file:
		for readline in open_file:
			read = readline.replace('\n','')
			token = read.split('\t')
			source = token[0]
			target = token[1]

			if source != "source" and target != "target":
				data_graph.add_edge(source, target)

	return data_graph

def get_unique_edges(topology_1_graph, topology_2_graph, topology_3_graph):

	topology_1_uniq_set = list(set(topology_1_graph.edges()) - set(topology_2_graph.edges()))
	topology_1_uniq_set = list(set(topology_1_uniq_set) - set(topology_3_graph.edges()))

	return topology_1_uniq_set

def get_counterwise_edges(topology_1_graph, topology_2_graph):

	topology_1_common_set = list(set(topology_1_graph.edges()) & set(topology_2_graph.edges()))

	return topology_1_common_set

def get_ra_unique_edges(topology_1_graph, topology_2_graph, topology_3_graph):

	ra_common_set = list(set(topology_1_graph.edges()) & set(topology_2_graph.edges()))
	ra_uniq_set = list(set(ra_common_set) - set(topology_3_graph.edges()))

	return ra_uniq_set

def cleanup_graph(edge_list):

	data_graph = nx.Graph()

	for i in range(len(edge_list)):
		edge = edge_list[i]
		source = edge[0]
		target = edge[1]
		data_graph.add_edge(source, target)

	data_graph = nx.Graph()
	data_graph.add_edges_from(edge_list)
	data_graph.to_undirected()

	return data_graph
		
def write_output(output_name, output_type, input_list):
	
	#STEP1: write full topology
	output_file = '%s.%s.topology.tsv' % (output_name, output_type)
	output_txt = open(output_file,'w')
	output_txt.write('target\tsource\n')

	for i in range(len(input_list)):
		edge = input_list[i]
		output_txt.write('%s\t%s\n' % (edge[0], edge[1]))

	output_txt.close()

	#STEP2: write sub topology
	data_graph = cleanup_graph(input_list)
	data_graph.to_undirected()

	#STEP4: write log file to characterize topology
	output_file = '%s.%s.topology.log' % (output_name, output_type)
	output_txt = open(output_file,'w')
	output_txt.write('%s.%s node size: %s\n' % (output_name, output_type, len(data_graph.nodes())))
	output_txt.write('%s.%s edge size: %s\n' % (output_name, output_type, len(data_graph.edges())))

	protein_list = []
	autoantibody_list = []
	metabolite_list = []

	node_list = list(data_graph.nodes())

	for node in node_list:
		if 'p_' == node[0:2]:
			protein_list.append(node)
		elif 'aa_' == node[0:3]:
			autoantibody_list.append(node)
		else:
			metabolite_list.append(node)
	output_txt.write('Total proteins: %s\n' % len(protein_list))
	output_txt.write('Total autoantibodies: %s\n' % len(autoantibody_list))
	output_txt.write('Total metabolites: %s\n' % len(metabolite_list))
	output_txt.close()

if __name__ == "__main__":

	import sys
	import networkx as nx

	#load network_topologys (six in total)
	topology_1_name = sys.argv[1] 
	topology_2_name = sys.argv[2] 
	topology_3_name = sys.argv[3] 

	topology_1_pos_file = '../topology_data_scenario_padj0.05/%s.corr.pad.sig.pos.topology.tsv' % topology_1_name
	topology_2_pos_file = '../topology_data_scenario_padj0.05/%s.corr.pad.sig.pos.topology.tsv' % topology_2_name
	topology_3_pos_file = '../topology_data_scenario_padj0.05/%s.corr.pad.sig.pos.topology.tsv' % topology_3_name
	
	topology_1_neg_file = '../topology_data_scenario_padj0.05/%s.corr.pad.sig.neg.topology.tsv' % topology_1_name
	topology_2_neg_file = '../topology_data_scenario_padj0.05/%s.corr.pad.sig.neg.topology.tsv' % topology_2_name
	topology_3_neg_file = '../topology_data_scenario_padj0.05/%s.corr.pad.sig.neg.topology.tsv' % topology_3_name

	topology_1_pos_graph = init_topolgy_graph(topology_1_pos_file)
	topology_2_pos_graph = init_topolgy_graph(topology_2_pos_file)
	topology_3_pos_graph = init_topolgy_graph(topology_3_pos_file)

	topology_1_neg_graph = init_topolgy_graph(topology_1_neg_file)
	topology_2_neg_graph = init_topolgy_graph(topology_2_neg_file)
	topology_3_neg_graph = init_topolgy_graph(topology_3_neg_file)

	print ("#INPUT: %s, nodes: %s, edges: %s" % (topology_1_pos_file, len(topology_1_pos_graph.nodes()), len(topology_1_pos_graph.edges())))
	print ("#INPUT: %s, nodes: %s, edges: %s" % (topology_2_pos_file, len(topology_2_pos_graph.nodes()), len(topology_2_pos_graph.edges())))
	print ("#INPUT: %s, nodes: %s, edges: %s" % (topology_3_pos_file, len(topology_3_pos_graph.nodes()), len(topology_3_pos_graph.edges())))

	print ("#INPUT: %s, nodes: %s, edges: %s" % (topology_1_neg_file, len(topology_1_neg_graph.nodes()), len(topology_1_neg_graph.edges())))
	print ("#INPUT: %s, nodes: %s, edges: %s" % (topology_2_neg_file, len(topology_2_neg_graph.nodes()), len(topology_2_neg_graph.edges())))
	print ("#INPUT: %s, nodes: %s, edges: %s" % (topology_3_neg_file, len(topology_3_neg_graph.nodes()), len(topology_3_neg_graph.edges())))

	#Check list #1
	#Objective: find whether edge in network_topology_1 is unique compared to other network topologies
	#Objective: find whether edge in network_topology_2 is unique compared to other network topologies
	#Objective: find whether edge in network_topology_3 is unique compared to other network topologies
	#pos
	topology_1_pos_uniq_list = get_unique_edges(topology_1_pos_graph, topology_2_pos_graph, topology_3_pos_graph)
	topology_2_pos_uniq_list = get_unique_edges(topology_2_pos_graph, topology_1_pos_graph, topology_3_pos_graph)
	topology_3_pos_uniq_list = get_unique_edges(topology_3_pos_graph, topology_1_pos_graph, topology_2_pos_graph)
	#neg
	topology_1_neg_uniq_list = get_unique_edges(topology_1_neg_graph, topology_2_neg_graph, topology_3_neg_graph)
	topology_2_neg_uniq_list = get_unique_edges(topology_2_neg_graph, topology_1_neg_graph, topology_3_neg_graph)
	topology_3_neg_uniq_list = get_unique_edges(topology_3_neg_graph, topology_1_neg_graph, topology_2_neg_graph)

	#outputs
	write_output(topology_1_name, 'pos.uniq', topology_1_pos_uniq_list)
	write_output(topology_1_name, 'neg.uniq', topology_1_neg_uniq_list)

	write_output(topology_2_name, 'pos.uniq', topology_2_pos_uniq_list)
	write_output(topology_2_name, 'neg.uniq', topology_2_neg_uniq_list)

	write_output(topology_3_name, 'pos.uniq', topology_3_pos_uniq_list)
	write_output(topology_3_name, 'neg.uniq', topology_3_neg_uniq_list)

	#Objective: find whether edge in network_topology_1 & network_topology 2 is common; and is not common in network_topology_3
	#Objective: find whether edge in network_topology_2 is unique compared to other network topologies
	#Objective: find whether edge in network_topology_2 is unique compared to other network topologies
	ra_pos_uniq_list = get_ra_unique_edges(topology_1_pos_graph, topology_2_pos_graph, topology_3_pos_graph)
	ra_neg_uniq_list = get_ra_unique_edges(topology_1_neg_graph, topology_2_neg_graph, topology_3_neg_graph)

	write_output('ra', 'pos.uniq', ra_pos_uniq_list)
	write_output('ra', 'neg.uniq', ra_neg_uniq_list)

	#Check list #3
	#find counter-wise trend (for example, positive rho in ACPA-pos, negative rho in ACPA-neg)
	#Objective: find whether edge in network_topology_1 al
	#positive rho: ACPA-pos, negative rho in ACPA-neg
		#does this exist in control?
	#negative rho: ACPA-pos, positive rho in ACPA-neg
		#does this exist in control?
	topology_1_neg_counterwise_list = get_counterwise_edges(topology_1_neg_graph, topology_2_pos_graph)
	topology_1_pos_counterwise_list = get_counterwise_edges(topology_1_pos_graph, topology_2_neg_graph)

	print (len(topology_1_neg_counterwise_list))
	print (len(topology_1_pos_counterwise_list))
	write_output(topology_1_name, 'neg.counter.common', topology_1_neg_counterwise_list)
	write_output(topology_1_name, 'pos.counter.common', topology_1_pos_counterwise_list)

	topology_2_neg_counterwise_list = get_counterwise_edges(topology_2_neg_graph, topology_1_pos_graph)
	topology_2_pos_counterwise_list = get_counterwise_edges(topology_2_pos_graph, topology_1_neg_graph)

	print (len(topology_2_neg_counterwise_list))
	print (len(topology_2_pos_counterwise_list))
	write_output(topology_2_name, 'neg.counter.common', topology_2_neg_counterwise_list)
	write_output(topology_2_name, 'pos.counter.common', topology_2_pos_counterwise_list)

