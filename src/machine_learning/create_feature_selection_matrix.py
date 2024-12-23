#"create_feature_selection_matrix.py"     22.01.05

#Feature selection based on RWR results.
#[IMPORTANT NOTE] 
#This script is designed to handle two cutoffs. 
#[1] Top N %  ; you must defined this with "p"; such as 10p (for top 10 percent), 50p (for top 50 percent)
#[2] Top N  ; you must define this as "top"; such as top10 (for top 10), top1000 (for top 1000)

#Intended inputs: outputs from "RWR.R"; which is "kfold.RWR.result.txt"

def get_RWR_features(file_name, cutoff):

	data_df = pd.read_csv(file_name, sep ="\t", header=None)
	r, c = data_df.shape

	threshold = define_cutoff(r, cutoff)
	print (threshold)
	feature_list = []

	count = 0
	class_list = ["control","acpa_pos","acpa_neg"]

	for i in range(r):
		if count < threshold:
			feature = data_df.iloc[i,0]
			if feature not in class_list:
				feature_list.append(feature)
				count += 1
		else:
			break

	print (count)

	return feature_list

def define_cutoff(N, cutoff):

	if 'top' in cutoff:
		threshold = cutoff.split('top')[1]
		threshold = float(threshold)

	else:
		threshold = cutoff.split('p')[0]
		threshold = float(threshold)
		threshold = N * threshold * 0.01 

	return int(threshold)

def create_feature_selected_matrix(data_matrix_dir, RWR_feature_list, output_dir):

	data_file = 'multiplex'

	train_file = '%s/%s.train.tsv' % (data_matrix_dir, data_file)
	test_file = '%s/%s.test.tsv' % (data_matrix_dir, data_file)

	#[1] matrix to dict
	train_data_dict, train_feature_list, train_patient_ID_list = make_dict_from_profile(train_file)
	test_data_dict, test_feature_list, test_patient_ID_list = make_dict_from_profile(test_file)

	#[2] write output with only selected features
	write_fs_text(train_data_dict, train_feature_list, RWR_feature_list, train_patient_ID_list, output_dir, 'multiplex.fs.train.tsv')
	write_fs_text(test_data_dict, test_feature_list, RWR_feature_list, test_patient_ID_list, output_dir, 'multiplex.fs.test.tsv')

def make_dict_from_profile(data_file):

	data_dict = {}
	data_df = pd.read_csv(data_file, sep='\t', index_col=0)

	patient_ID_list = data_df.columns.values
	feature_list = data_df.index.values
	cleaned_feature_list = [] #this is because original matrix contains white spaces, primes, etc; I had to change these for proper table load during RWR.R
	r, c = data_df.shape

	for i in range(r):
		feature = feature_list[i]

		feature = feature.replace(' ','_')
		feature = feature.replace('-','_')
		feature = feature.replace(',','_') #newly added sep18
		feature = feature.replace("'",'prime')
		feature = feature.replace("*",'')
		cleaned_feature_list.append(feature)

		for j in range(c):
			patient_ID = patient_ID_list[j]
			#value = data_df.iloc[i][j]
			value = data_df.iloc[i, j]
			data_dict[feature, patient_ID] = value

	return data_dict, cleaned_feature_list, patient_ID_list

def write_fs_text(data_dict, feature_list, RWR_feature_list, patient_ID_list, output_dir, output_str):

	output_file = '%s/%s' % (output_dir, output_str)
	output_txt = open(output_file, 'w')
	
	#write header (patient IDs)
	for patient_ID in patient_ID_list:
		output_txt.write('\t%s' % patient_ID)
	output_txt.write('\n')

	for feature in feature_list:
		if feature in RWR_feature_list or feature == "acpa":
			output_txt.write('%s' % feature)
			for patient_ID in patient_ID_list:
				value = data_dict[feature, patient_ID]
				output_txt.write('\t%s' % value)
			output_txt.write('\n')
	output_txt.close()

if __name__ == '__main__':
	import sys
	import pandas as pd
	import os
	import math
	import numpy as np

	#Buffers
	RWR_result_file = sys.argv[1]
	data_matrix_dir = sys.argv[2] #where the kfold/train, kfold/test matrix are stored

	cutoff = sys.argv[3] #cutoffs for top N features or top n% features

	output_folder_name = sys.argv[4] #feature selected matrix will be stored here
	kfold = sys.argv[5] #kfold to consider

	cutoff_dir = '%s/%s' % (output_folder_name, cutoff)
	kfold_output_dir = '%s/%s/%s' % (output_folder_name, cutoff, kfold)

	#mange directories
	if os.path.isdir(cutoff_dir) == False:
		os.system('mkdir %s' % (cutoff_dir))
	if os.path.isdir(kfold_output_dir) == False:
		os.system('mkdir %s' % (kfold_output_dir))

	#start 
	RWR_feature_list = get_RWR_features(RWR_result_file, cutoff)
	create_feature_selected_matrix(data_matrix_dir, RWR_feature_list, kfold_output_dir)
		
