#STEP4_topology_with_threshold.py   22.11.22

#from outputs from STEP3_update_topology_pad.py
# *.corr.padj.topology.tsv

#parse target-source information that only passes certain threshold

#input from: analysis/correlation_network/topology_data
#output stored: analysis/correlation_network/topology_data

#designed to be runned by: get_sig_network.sh

def get_num_readlines(data_file):
    with open(data_file) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def main(topology_file, rho_threshold, pad_threshold, output_file):
#note avoid using pd dataframe due to memory shortage

	len_readlines = get_num_readlines(topology_file)

	output_txt = open(output_file, 'w')
	output_txt.write('source\ttarget\trho\tpval\tpad\n')
	
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
						output_txt.write('%s\t%s\t%s\t%s\t%s\n' % (source, target, rho, pval, padj))

	output_txt.close()

if __name__ == "__main__":

	import pandas as pd
	import statsmodels.stats.multitest as smm
	import sys
	import os

	file_dir = "../../../analysis/correlation_network/topology_data_scenario_padj0.05"
	#file_list = ["acpa_neg_3_omics","acpa_pos_3_omics", "control_3_omics"]

	rho_threshold = 0.7
	pad_threshold = 0.001

	file_name = sys.argv[1]

	topology_file = '%s/%s.corr.pad.topology.tsv' % (file_dir, file_name)
	output_file = '%s/%s.corr.pad.sig.topology.tsv' % (file_dir, file_name)    

	if os.path.exists(output_file):
		os.remove(output_file)
	else:
		print ("we detected output file from previous run. removing this file")

	main(topology_file, rho_threshold, pad_threshold, output_file)

	print ("Job finished:%s" % output_file)
