#cleanup_RWR_ready_file.py   22.01.05
#
#This script is desgined to handle problem that I found as below:
#> I found that kfold.topology.tsv was not being loaded as a table by R (for RWR.R)
#  This is because there are (blanks; `; ,;  *) in the feature names.
#  I will have to force changing these special characters into _
#
#Intended input: output from "integrate_network.v2.py"; which is Kfold.topology.tsv

import sys

input_data_file = sys.argv[1]
output_data_file = sys.argv[2]

input_data_open = open(input_data_file,'r')
input_data_readlines = input_data_open.readlines()

output_txt = open(output_data_file,'w')

for i in range(len(input_data_readlines)):
	read = input_data_readlines[i]
	read = read.replace('\n','')
	token = read.split('\t')

	if i == 0: #header
		for j in range(1, len(token)):
			feature_name = token[j]
			feature_name = feature_name.replace(' ','_')
			feature_name = feature_name.replace('-','_')
			feature_name = feature_name.replace("'",'prime')
			feature_name = feature_name.replace("*",'')
			feature_name = feature_name.replace(",",'_')
			output_txt.write('\t%s' % feature_name)

	if i > 0:
		feature_name = token[0]
		feature_name = feature_name.replace(' ','_')
		feature_name = feature_name.replace('-','_')
		feature_name = feature_name.replace("'",'prime')
		feature_name = feature_name.replace("*",'')
		feature_name = feature_name.replace(",",'_')
		output_txt.write('%s' % feature_name)

		for j in range(1, len(token)):
			value = token[j]
			output_txt.write('\t%s' % value) 
	output_txt.write('\n')

output_txt.close()

	



