#STEP2_make_sigNcorr_results.   22.11.16

#from the outputs from "STEP1_condition_specific_correlation":
#[1] *.corr.rho.tsv
#[2] *.corr.sig.tsv

#make a single file with a format of source-target
#output: *.corr.topology.tsv

import pandas as pd
import sys

def main(rho_file, sig_file, output_file):
    
	#make topology_dict[source, target] = [rho, pval]
	topology_dict = {}
	key_list = []
	pval_list = [] #list for later adjustment
	
	rho_df = pd.read_csv(rho_file, sep="\t", index_col=0)
	sig_df = pd.read_csv(sig_file, sep="\t", index_col=0)
	
	feature_list = rho_df.index.values
	r, c = rho_df.shape

	output_txt = open(output_file ,'w')
	output_txt.write('source\ttarget\trho\tpval\n')
   
	for i in range(r):
		source = feature_list[i]
		for j in range(c):
			target = feature_list[j]
			
			#Do not consider self-target, reverse correlation (meaningless)
			if source != target:
				try: 
					rho_value = topology_dict[(source, target)][0]
					sig_value = topology_dict[(source, target)][1]
					None
				except KeyError:
					try: 
						rho_value = topology_dict[(target, source)][0]
						sig_value = topology_dict[(target, source)][1]
						None
					except KeyError:
						rho_value = rho_df.iloc[i][j]
						sig_value = sig_df.iloc[i][j]
						topology_dict[(source, target)] = [rho_value, sig_value]
						output_txt.write('%s\t%s\t%s\t%s\n' % (source, target, rho_value, sig_value))
								
	output_txt.close()


file_dir = "../../analysis/correlation_network"
# file_list = ["acpa_neg_3_omics","acpa_pos_3_omics", "control_3_omics"]

file_name = sys.argv[1]

rho_file = '%s/%s.corr.rho.tsv' % (file_dir, file_name)
sig_file = '%s/%s.corr.sig.tsv' % (file_dir, file_name)

output_file = '%s/%s.corr.topology.tsv' % (file_dir, file_name)    

topology_dict = main(rho_file, sig_file, output_file)
