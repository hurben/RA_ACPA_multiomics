#update_subnetwork_topology_file.py			22.04.25
#
# -> which can be done by "find_subnetwork_from_cyto_file.py"
#

#output file contains 
#---------------------------------------------------------------------------

#make topology info from protein GSE
def make_topology_info_from_protein_gse(data_file):

	goterm_dict = {}
	data_df = pd.read_csv(data_file, sep="\t")
	r,c = data_df.shape

	for i in range(r):
		goterm = data_df["Term"][i]
		goterm = goterm.split('~')[1]

		pval = data_df["PValue"][i]
		gene_list_str = data_df["Genes"][i]
		gene_list = gene_list_str.split(',')

		if pval < 0.05:
			goterm_dict[goterm] = gene_list

	return goterm_dict

#make topology info from metabolites GSE
def make_topology_info_from_metabolite_gse(data_file):

	pathway_dict = {}
	data_df = pd.read_csv(data_file, sep="\t")
	r,c = data_df.shape

	for i in range(r):
		pathway = data_df["pathway"][i]
		pval = data_df["pvalue"][i]
		element_str = data_df["elements"][i]
		element_list = element_str.split(',')

		if pval < 0.05:
			pathway_dict[pathway] = element_list

	return pathway_dict

def write_output(subnetwork_topology_file, goterm_dict, pathway_dict, output_file):
	
	open_original_topology = open(subnetwork_topology_file, 'r')
	original_topology_readlines = open_original_topology.readlines()

	output_txt = open(output_file, 'w')

	#copy contents
	for i in range(len(original_topology_readlines)):
		read = original_topology_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')
		source = token[0]
		target = token[1]
		if 'p_' in source:
			source = source.split('_')[1]
		if 'p_' in target:
			target = target.split('_')[1]

		if i == 0:
			output_txt.write('%s\t%s\tedge_type\n' % (source, target))
		else:
			output_txt.write('%s\t%s\t1\n' % (source, target))
	
	for source in list(goterm_dict.keys()):
		element_list = goterm_dict[source]
		for target in element_list:
			target = target.replace(' ','')
			output_txt.write('%s\t%s\t0\n' % (source, target))
	
	for source in list(pathway_dict.keys()):
		element_list = pathway_dict[source]
		for target in element_list:
			target = target.replace(' ','')
			output_txt.write('%s\t%s\t0\n' % (source, target))

	open_original_topology.close()
	output_txt.close()

#make outputfile (extend original topology file)

if __name__ == "__main__":

	import sys
	import pandas as pd
	import statistics
	import math

	subnetwork_topology_file = sys.argv[1]
	output_file = '%s.v2.tsv' % subnetwork_topology_file.split('.tsv')[0]
	print (output_file)

	protein_gse_file = '../../../analysis/full_data/cytoscape/gse/GSE_proteomics.v2.txt'
	metabolite_gse_file = '../../../analysis/full_data/cytoscape/gse/metabolomics.hypergeometric.result.tsv'

	goterm_dict = make_topology_info_from_protein_gse(protein_gse_file)
	pathway_dict = make_topology_info_from_metabolite_gse(metabolite_gse_file)
	write_output(subnetwork_topology_file, goterm_dict, pathway_dict, output_file)
	
	print (pathway_dict)


