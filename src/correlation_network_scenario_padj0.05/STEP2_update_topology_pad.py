#STEP3_update_topology_pad.py 22.11.21

#from the outputs from "STEP2_condition_specific_correlation":
# *.corr.topology.tsv

#update the input file by including padj values (BH-adjusted pvalue)
# *.corr.padj.topology.tsv

#input from: analysis/correlation_network/topology_data
#output stored: analysis/correlation_network/topology_data

#designed to be runned by: pbs.padj.batch1.sh pbs.padj.batch2.sh pbs.padj.batch3.sh


def main(topology_file, output_file):

	topology_df = pd.read_csv(topology_file, sep = "\t")
	r, c = topology_df.shape

	pval_list = []

	for i in range(r):
		pval = topology_df["pval"][i]
		pval_list.append(pval)

	padj_list = list(smm.multipletests(pval_list, method ='fdr_bh')[1])

	output_txt = open(output_file, 'w')
	output_txt.write('source\ttarget\trho\tpval\tpad\n')

	for i in range(r):
		source = topology_df["source"][i]
		target = topology_df["target"][i]
		rho = topology_df["rho"][i]
		pval = topology_df["pval"][i]
		padj = padj_list[i]
		output_txt.write('%s\t%s\t%s\t%s\t%s\n' % (source, target, rho, pval, padj))

	output_txt.close()

if __name__ == "__main__":

	import pandas as pd
	import statsmodels.stats.multitest as smm
	import sys

	file_dir = "../../../analysis/correlation_network/topology_data_scenario_padj0.05"
	#file_list = ["acpa_neg_3_omics","acpa_pos_3_omics", "control_3_omics"]

	file_name = sys.argv[1]

	topology_file = '%s/%s.corr.topology.tsv' % (file_dir, file_name)
	output_file = '%s/%s.corr.pad.topology.tsv' % (file_dir, file_name)    

	main(topology_file, output_file)
