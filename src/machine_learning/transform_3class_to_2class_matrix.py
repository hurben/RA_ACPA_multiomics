#"transform_3class_to_2class_matrix.py"
#
#The datamatrix is currently in 3 class (0: control, 1: acpa-positive, 2: acpa-negative)
#We need to change this in to two class (i.e., control vs. RA, control vs. acpa-positive, control vs. acpa-negative) for binary classification.
#
#Intended inputs: outputs from "machine_learning/create_feature_selection_matrix.py"; which makes datamatrix from the ACPA-centric subnetwork using RWR.

def make_output(data_file, output_file, class_of_interest):

	data_dict = {}
	selective_patient_ID_list = [] #this list will record class_beta. patientIDs that does not fall into this list will become other class

	class_alpha = int(class_of_interest.split('_')[0]) 
	class_beta = int(class_of_interest.split('_')[1]) 

	data_df = pd.read_csv(data_file, sep="\t", index_col = 0)
	r, c = data_df.shape

	feature_list = data_df.index.values
	patient_ID_list = data_df.columns.values

	for i in range(r):
		feature = feature_list[i]
		for j in range(c):
			patient_ID = patient_ID_list[j]
			value = data_df.iloc[i][j]
			data_dict[feature, patient_ID] = value

	for patient_ID in patient_ID_list:
		value = data_dict['acpa', patient_ID]
		if class_beta == 3: #This is specifically designed to consider 0 vs 1,2; append all
			selective_patient_ID_list.append(patient_ID)
		else:
			if value == class_alpha or value == class_beta: #designed to consider 0 vs 1, 0 vs 2, 1 vs 2
				selective_patient_ID_list.append(patient_ID)

	output_txt = open(output_file,'w')
	#write headers
	for patient_ID in selective_patient_ID_list:
		output_txt.write('\t%s' % patient_ID)
	output_txt.write('\n')
	
	for feature in feature_list:
		output_txt.write(feature)
		if feature == 'acpa':
		#write, or transfrom acpa values if necessary
			for patient_ID in selective_patient_ID_list:
				acpa = data_dict[feature, patient_ID]

				if class_of_interest  == "0_3": 
					if acpa == 2 or acpa == 1:
						value = 'ra'
					else:
						value = 'control'

				else:
					if acpa == 1:
						value = 'pos'
					if acpa == 2:
						value = 'neg'
					if acpa == 0:
						value = 'control'

				output_txt.write('\t%s' % (value))
		else:	
		#write other feature values
			for patient_ID in selective_patient_ID_list:
				value = data_dict[feature, patient_ID]
				output_txt.write('\t%s' % value)

		output_txt.write('\n')

	output_txt.close()


if __name__ == '__main__':

	import pandas as pd
	import os
	import sys

	fs_input_dir = sys.argv[1]
	total_kfold = int(sys.argv[2])

	class_of_interest = sys.argv[3]
	output_str = sys.argv[4]
	split_type= sys.argv[5]

	output_dir = '%s_%s' % (fs_input_dir, output_str)

	if split_type == 'percentage':
		split_list = ["1p", "5p", "10p", "20p", "25p", "30p", "40p", "50p","100p"]
	if split_type == 'topn':
		split_list = ["top10", "top20", "top30", "top40", "top50", "top60", "top70", "top80", "top90", "top100","top200","top300","top400","top500","top600", "top700","top800","top900","top1000"]

	if os.path.isdir(output_dir) == False:
		os.system('mkdir %s' % output_dir)
	else:
		os.system('rm -r %s' % output_dir)
		os.system('mkdir %s' % output_dir)

	for split in split_list:

		output_split_dir = '%s/%s' % (output_dir, split)
		os.system('mkdir %s' % output_split_dir)

		for k in range(total_kfold):
			kfold = '%sfold' % (k + 1)
			print (split, kfold)
			output_split_kfold_dir = '%s/%s' % (output_split_dir, kfold)
			os.system('mkdir %s' % output_split_kfold_dir)

			fs_train_data_file = '%s/%s/%s/multiplex.fs.train.tsv' % (fs_input_dir, split, kfold)
			fs_test_data_file = '%s/%s/%s/multiplex.fs.test.tsv' % (fs_input_dir, split, kfold)

			fs_train_data_output_file = '%s/multiplex.fs.train.tsv' % (output_split_kfold_dir)
			fs_test_data_output_file = '%s/multiplex.fs.test.tsv' % (output_split_kfold_dir)
			make_output(fs_train_data_file, fs_train_data_output_file, class_of_interest)
			make_output(fs_test_data_file, fs_test_data_output_file, class_of_interest)
