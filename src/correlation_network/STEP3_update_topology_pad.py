#STEP2_make_sigNcorr_results.   22.11.16

#from the outputs from "STEP1_condition_specific_correlation":
#[1] *.corr.rho.tsv
#[2] *.corr.sig.tsv

#make a single file that find significant correlation (defined by user)
#output: *.corr.rho.sig.tsv


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


	file_dir = "../../analysis/correlation_network"
	#file_list = ["acpa_neg_3_omics","acpa_pos_3_omics", "control_3_omics"]

	file_name = sys.argv[1]

	topology_file = '%s/%s.corr.topology.tsv' % (file_dir, file_name)
	output_file = '%s/%s.corr.pad.topology.tsv' % (file_dir, file_name)    

	main(topology_file, output_file)
