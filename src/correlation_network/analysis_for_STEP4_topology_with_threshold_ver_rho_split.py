#STEP4_topology_with_threshold_ver_rho_split.py   22.12.05

#from outputs from STEP3_update_topology_pad.py
# *.corr.padj.topology.tsv

#[modified]: split outputs that has positive rho and negative rho

#parse target-source information that only passes certain threshold

def get_num_readlines(data_file):
    with open(data_file) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def main(topology_file, output_name):
#note avoid using pd dataframe due to memory shortage

	sig_correlation_count_dict = {}
	pval_count_dict = {}
	rho_count_dict = {}

	pval_bin_list = [0.00001, 0.0001, 0.001, 0.01, 0.05, 0.1, 1]
	pos_rho_bin_list = list(np.round(np.linspace(0,1,11),2))
	neg_rho_bin_list = list(np.round(np.linspace(-1,0,11),2))

	#init sig_correlation_count_dict
	for pval_bin in pval_bin_list:
		pval_count_dict[pval_bin] = 0
		for pos_rho_bin in pos_rho_bin_list:
			sig_correlation_count_dict[pval_bin, pos_rho_bin] = 0
		for neg_rho_bin in neg_rho_bin_list:
			sig_correlation_count_dict[pval_bin, neg_rho_bin] = 0

	for pos_rho_bin in pos_rho_bin_list:
		rho_count_dict[pos_rho_bin] = 0
	for neg_rho_bin in neg_rho_bin_list:
		rho_count_dict[neg_rho_bin] = 0

	len_readlines = get_num_readlines(topology_file)

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
				padj = float(token[4])

				for pval_bin in pval_bin_list:
					if padj < pval_bin:
						pval_count_dict[pval_bin] += 1
						for pos_rho_bin in pos_rho_bin_list:
							if rho > pos_rho_bin:
								sig_correlation_count_dict[pval_bin, pos_rho_bin] += 1

						for neg_rho_bin in neg_rho_bin_list:
							if rho < neg_rho_bin:
								sig_correlation_count_dict[pval_bin, neg_rho_bin] += 1

				for pos_rho_bin in pos_rho_bin_list:
					if rho > pos_rho_bin:
						rho_count_dict[pos_rho_bin] += 1

				for neg_rho_bin in neg_rho_bin_list:
					if rho < neg_rho_bin:
						rho_count_dict[neg_rho_bin] += 1


	output_file = '%s.rho.padj.characteristics.tsv' % output_name
	output_txt = open(output_file,'w')
	output_txt.write('PADJ\tRHO\tCOUNT\n')
	for pval_bin in pval_bin_list:
		for pos_rho_bin in pos_rho_bin_list:
			count = sig_correlation_count_dict[pval_bin, pos_rho_bin]
			output_txt.write('%s\t%s\t%s\n' % (pval_bin, pos_rho_bin, count))

		for neg_rho_bin in neg_rho_bin_list:
			count = sig_correlation_count_dict[pval_bin, neg_rho_bin]
			output_txt.write('%s\t%s\t%s\n' % (pval_bin, neg_rho_bin, count))
	output_txt.close()

	output_file = '%s.rho.characteristics.tsv' % output_name
	output_txt = open(output_file,'w')
	output_txt.write('RHO\tCOUNT\tTREND\n')
	for pos_rho_bin in pos_rho_bin_list:
		count = rho_count_dict[pos_rho_bin]
		output_txt.write('%s\t%s\tpos\n' % (pos_rho_bin, count))

	for neg_rho_bin in neg_rho_bin_list:
		count = rho_count_dict[neg_rho_bin]
		output_txt.write('%s\t%s\tneg\n' % (neg_rho_bin, count))
	output_txt.close()

	output_file = '%s.padj.characteristics.tsv' % output_name
	output_txt = open(output_file,'w')
	output_txt.write('PADJ\tCOUNT\n')
	for pval_bin in pval_bin_list:
		count = pval_count_dict[pval_bin]
		output_txt.write('%s\t%s\n' % (pval_bin, count))
	output_txt.close()

if __name__ == "__main__":

	import pandas as pd
	import numpy as np
	import statsmodels.stats.multitest as smm
	import sys
	import os

	topology_file = sys.argv[1]
	output_name = sys.argv[2]
	main(topology_file, output_name)

