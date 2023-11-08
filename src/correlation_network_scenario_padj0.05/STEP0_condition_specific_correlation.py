#STEP1_condition_specific_correlation     22.11.10

#do correlation, split results into two files
#file1: rho value
#file2: p value

import pandas as pd
from scipy import stats
import statistics
import numpy as np


def main(data_file, output_file):

    data_df = pd.read_csv(data_file, sep ="\t", index_col=0)
    data_df = data_df.T #transposing the data for simplicity
    
    rho_output_file = output_file.replace('.tsv', '.corr.rho.tsv')
    sig_output_file = output_file.replace('.tsv', '.corr.sig.tsv')
    
    rho_output_txt = open(rho_output_file,'w')
    sig_output_txt = open(sig_output_file,'w')
    
    feature_list = list(data_df.columns.values)
    
    write_headers(rho_output_txt, feature_list)
    write_headers(sig_output_txt, feature_list)
    
    for feature_alpha in feature_list: #row
        feature_alpha_value_list = list(data_df[feature_alpha])
        
        rho_output_txt.write(feature_alpha)
        sig_output_txt.write(feature_alpha)
        
        for feature_beta in feature_list: #column
            feature_beta_value_list = list(data_df[feature_beta])
            if feature_alpha == feature_beta:
                rho_output_txt.write('\tnan')
                sig_output_txt.write('\tnan')
            else:
                rho, pval = stats.spearmanr(feature_alpha_value_list, feature_beta_value_list, nan_policy="omit")
                # print (feature_alpha, feature_beta)
                # print (rho, pval)
                rho_output_txt.write('\t%s' % rho)
                sig_output_txt.write('\t%s' % pval)
        rho_output_txt.write('\n')
        sig_output_txt.write('\n')

    rho_output_txt.close()
    sig_output_txt.close()
    
def write_headers(output_txt, feature_list):
    for feature_name in feature_list:
        output_txt.write('\t%s' % feature_name)
    output_txt.write('\n')


data_file = '../../../analysis/correlation_network/preprocessed_data/acpa_neg_3_omics.tsv'
output_file = '../../../analysis/correlation_network/topology_data_scenario_padj0.05/acpa_neg_3_omics.tsv'
main(data_file, output_file)

data_file = '../../../analysis/correlation_network/preprocessed_data/acpa_pos_3_omics.tsv'
output_file = '../../../analysis/correlation_network/topology_data_scenario_padj0.05/acpa_pos_3_omics.tsv'
main(data_file, output_file)


