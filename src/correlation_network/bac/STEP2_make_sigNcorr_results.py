#STEP2_make_sigNcorr_results.   22.11.16

#from the outputs from "STEP1_condition_specific_correlation":
#[1] *.corr.rho.tsv
#[2] *.corr.sig.tsv

#make a single file that find significant correlation (defined by user)
#output: *.corr.rho.sig.tsv

import pandas as pd
import statsmodels.stats.multitest as smm
import sys

def main(rho_file, sig_file):
    
    #make topology_dict[source, target] = [rho, pval]
    topology_dict = {}
    key_list = []
    pval_list = [] #list for later adjustment
    
    rho_df = pd.read_csv(rho_file, sep="\t", index_col=0)
    sig_df = pd.read_csv(sig_file, sep="\t", index_col=0)
    
    feature_list = rho_df.index.values
    r, c = rho_df.shape
    
    for i in range(r):
        if (i % 1000 == 0):
            print (i)        
        source = feature_list[i]
        for j in range(c):
            target = feature_list[j]
            
            #Do not consider self-target, reverse correlation (meaningless)
            if source != target:
                if (source,target) not in list(topology_dict.keys()):
                    if (target,source) not in list(topology_dict.keys()):
                        
                        rho_value = rho_df.iloc[i][j]
                        sig_value = sig_df.iloc[i][j]
                        
                        topology_dict[source, target] = [rho_value, sig_value]
                        key_list.append((source,target))
                        pval_list.append(sig_value)
                        
    padj_list = list(smm.multipletests(pval_list, method ='fdr_bh')[1])
    
    print ('DEBUGING, the three numbers should be the same')
    print (len(key_list), len(pval_list), len(padj_list))
    
    #update_topology_dict with padj
    for i in range(len(key_list)):
        key = key_list[i]
        padj_value = padj_list[i]
        
        topology_dict[key][1] = padj_value
           
    return topology_dict

file_dir = "../../analysis/correlation_network"
# file_list = ["acpa_neg_3_omics","acpa_pos_3_omics", "control_3_omics"]

file_name = sys.argv[1]

rho_file = '%s/%s.corr.rho.tsv' % (file_dir, file_name)
sig_file = '%s/%s.corr.sig.tsv' % (file_dir, file_name)

output_file = '%s/%s.padj.topology.tsv' % (file_dir, file_name)    

topology_dict = main(rho_file, sig_file)

output_txt = open(output_file ,'w')
output_txt.write('source\ttarget\trho\tpadj\n')

for key in list(topology_dict.keys()):
    source = key[0]
    target = key[1]
    
    rho = topology_dict[key][0]
    padj = topology_dict[key][1]
    output_txt.write('%s\t%s\t%s\t%s\n' % (source, target, rho, padj))
        
output_txt.close()



