#STEP4_topology_with_threshold_ver_rho_split.py   22.12.05

#from outputs from STEP3_update_topology_pad.py
# *.corr.padj.topology.tsv

#[modified]: split outputs that has positive rho and negative rho

#parse target-source information that only passes certain threshold

#input from: analysis/correlation_network/topology_data
#output stored: analysis/correlation_network/topology_data

#designed to be runned by: get_sig_network_posneg.sh


def get_num_readlines(data_file):
    with open(data_file) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def main(topology_file, rho_threshold, pad_threshold, output_pos_file, output_neg_file):
#note avoid using pd dataframe due to memory shortage

	len_readlines = get_num_readlines(topology_file)

	output_pos_txt = open(output_pos_file, 'w')
	output_neg_txt = open(output_neg_file, 'w')

	output_pos_txt.write('source\ttarget\trho\tpval\tpad\n')
	output_neg_txt.write('source\ttarget\trho\tpval\tpad\n')
	
	with open(topology_file) as topology_open:

		#for readline in topology_open:
		for i in range(len_readlines): #debug purpose
			line = next(topology_open)
			if i != 0: #line 0 is header
				line = line.replace('\n','')
				token = line.split('\t')

				source = token[0]
				target = token[1]
				rho = float(token[2])
				abs_rho = abs(rho)
				pval = float(token[3])
				padj = float(token[4])

				if abs_rho > rho_threshold:
					if padj < pad_threshold:
						if rho > 0:
							output_pos_txt.write('%s\t%s\t%s\t%s\t%s\n' % (source, target, rho, pval, padj))
						if rho < 0:
							output_neg_txt.write('%s\t%s\t%s\t%s\t%s\n' % (source, target, rho, pval, padj))

	output_pos_txt.close()
	output_neg_txt.close()

if __name__ == "__main__":

	import pandas as pd
	import statsmodels.stats.multitest as smm
	import sys
	import os

	file_dir = "../../../analysis/correlation_network/topology_data_scenario_padj0.05"
	#file_list = ["acpa_neg_3_omics","acpa_pos_3_omics", "control_3_omics"]

	rho_threshold = 0.4
#	rho_threshold = 0.0
	pad_threshold = 0.05

	file_name = sys.argv[1]

	topology_file = '%s/%s.corr.pad.topology.tsv' % (file_dir, file_name)
	output_pos_file = '%s/%s.corr.pad.sig.pos.topology.tsv' % (file_dir, file_name)    
	output_neg_file = '%s/%s.corr.pad.sig.neg.topology.tsv' % (file_dir, file_name)    

	if os.path.exists(output_pos_file) or os.path.exists(output_neg_file):
		os.remove(output_pos_file)
		os.remove(output_neg_file)
	else:
		print ("we detected output file from previous run. removing this file")

	main(topology_file, rho_threshold, pad_threshold, output_pos_file, output_neg_file)

	print ("Job finished:%s, %s" % (output_pos_file, output_neg_file))
