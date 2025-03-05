#cv_preperation.py				21.11.23

def merge_multiple_dict_main(PI_dict, M_dict, P_dict, PI_patient_list, PI_list, M_list, P_list):

	data_dict = {}
	feature_list = []

	data_dict, feature_list = merge_multiple_dict_sub(PI_dict, PI_list, data_dict, PI_patient_list, feature_list, 'PI')
	data_dict, feature_list = merge_multiple_dict_sub(M_dict, M_list, data_dict, PI_patient_list, feature_list, 'M')
	data_dict, feature_list = merge_multiple_dict_sub(P_dict, P_list, data_dict, PI_patient_list, feature_list,'P')

	return data_dict, feature_list

def merge_multiple_dict_main_p1(PI_dict, P_dict, PI_patient_list, PI_list, P_list):

	data_dict = {}
	feature_list = []

	data_dict, feature_list = merge_multiple_dict_sub(PI_dict, PI_list, data_dict, PI_patient_list, feature_list, 'PI')
	data_dict, feature_list = merge_multiple_dict_sub(P_dict, P_list, data_dict, PI_patient_list, feature_list,'P')

	return data_dict, feature_list

def merge_multiple_dict_main_p2(PI_dict, M_dict, P_dict, PI_patient_list, PI_list, M_list, P_list):

	data_dict = {}
	feature_list = []

	data_dict, feature_list = merge_multiple_dict_sub(PI_dict, PI_list, data_dict, PI_patient_list, feature_list, 'PI')
	data_dict, feature_list = merge_multiple_dict_sub(P_dict, P_list, data_dict, PI_patient_list, feature_list,'P')
	data_dict, feature_list = merge_multiple_dict_sub(M_dict, M_list, data_dict, PI_patient_list, feature_list, 'M')

	return data_dict, feature_list


def merge_multiple_dict_main_p3(PI_dict, M_dict, PI_patient_list, PI_list, M_list):

	data_dict = {}
	feature_list = []

	data_dict, feature_list = merge_multiple_dict_sub(PI_dict, PI_list, data_dict, PI_patient_list, feature_list, 'PI')
	data_dict, feature_list = merge_multiple_dict_sub(M_dict, M_list, data_dict, PI_patient_list, feature_list, 'M')

	return data_dict, feature_list

def merge_multiple_dict_main_c1p1(PI_dict, P_dict, PI_patient_list, PI_list, P_list):

	data_dict = {}
	feature_list = []

	data_dict, feature_list = merge_multiple_dict_sub(PI_dict, PI_list, data_dict, PI_patient_list, feature_list, 'PI')
	data_dict, feature_list = merge_multiple_dict_sub(P_dict, P_list, data_dict, PI_patient_list, feature_list,'P')

	return data_dict, feature_list

def merge_multiple_dict_main_c1p3(PI_dict, M_dict, PI_patient_list, PI_list, M_list):

	data_dict = {}
	feature_list = []

	data_dict, feature_list = merge_multiple_dict_sub(PI_dict, PI_list, data_dict, PI_patient_list, feature_list, 'PI')
	data_dict, feature_list  = merge_multiple_dict_sub(M_dict, M_list, data_dict, PI_patient_list, feature_list, 'M')

	return data_dict, feature_list


def merge_multiple_dict_sub(query_dict, query_list, main_dict, patientID_list, feature_list, data_type):

	for feature in query_list:
		feature_main = feature
		if data_type == 'P':
			feature_main = 'p_' + feature

		feature_list.append(feature_main)

		for patientID in patientID_list:
			value = query_dict[patientID, feature]
			main_dict[patientID,feature_main] = value
	
	return main_dict, feature_list


def create_kfold_dataset(main_dict, main_feature_list, patient_list, kfold):

	control_patient_list = []  #0 = control
	acpa_pos_patient_list = [] #1 = pos
	acpa_neg_patient_list = [] #2 = neg

	for patient_ID in patient_list:
		class_value = main_dict[patient_ID, 'acpa']
		if class_value == 0.0:
			control_patient_list.append(patient_ID)
		if class_value == 1.0:
			acpa_pos_patient_list.append(patient_ID)
		if class_value == 2.0:
			acpa_neg_patient_list.append(patient_ID)


	kfold_control_split_list = np.array_split(control_patient_list, kfold)
	kfold_acpa_pos_split_list = np.array_split(acpa_pos_patient_list, kfold)
	kfold_acpa_neg_split_list = np.array_split(acpa_neg_patient_list, kfold)
	#split_list = [ [test indexs 1] [test indexs 2] [test indexs 3] .... [test indexs 5]]
	#1fold test data = [test indexs 1]
	#1fold training data = [test indexs 2] .... [test indexs 5]

	kfold_train_list = [] #contains patient IDs
	kfold_test_list = []

	#test data: this is to balance classes
	for i in range(kfold):
		temp_test_list = []
		for patient_ID in kfold_control_split_list[i]:
			temp_test_list.append(patient_ID)
		for patient_ID in kfold_acpa_pos_split_list[i]:
			temp_test_list.append(patient_ID)
		for patient_ID in kfold_acpa_neg_split_list[i]:
			temp_test_list.append(patient_ID)
		kfold_test_list.append(temp_test_list)

	for i in range(kfold): #this loop represents test set
		temp_train_list = []

		for j in range(kfold): #this loop represents train set
			if j != i:
				for k in kfold_control_split_list[j]:
					temp_train_list.append(k)
				for k in kfold_acpa_pos_split_list[j]:
					temp_train_list.append(k)
				for k in kfold_acpa_neg_split_list[j]:
					temp_train_list.append(k)

		kfold_train_list.append(temp_train_list)


	for i in range(kfold):
		print ('####')
		print (i)
		print (kfold_train_list[i])
		print (kfold_test_list[i])
		print ('####')

	for ith_fold in range(kfold):
		print ("Process: %s-fold" % (ith_fold+1))
		kfold_dir = "%sfold" % (ith_fold + 1)

		if os.path.isdir(kfold_dir) == False:
			os.system('mkdir %s' % kfold_dir)

		initiate_output_writing(ith_fold, main_dict, main_feature_list, kfold_test_list, kfold_train_list)
	print ("-----------------")


def initiate_output_writing(ith_fold, main_dict, main_feature_list, kfold_split_list, kfold_train_list):

	output_file = "%sfold/multiplex.test.tsv" % (ith_fold + 1)

	test_sample_list = kfold_split_list[ith_fold]
	write_output_main(output_file, main_dict, main_feature_list, test_sample_list)

	output_file = "%sfold/multiplex.train.tsv" % (ith_fold + 1)

	#write main contents
	train_sample_list = kfold_train_list[ith_fold]

	for test_patientID in test_sample_list:
		if test_patientID in train_sample_list:
			print ('ERROR: test patient ID is also found in train sample list')
			print (ith_fold, combination_str)

	write_output_main(output_file, main_dict, main_feature_list, train_sample_list)

def write_output_main(output_file, feature_dict, feature_list, sample_list):

	output_txt = open(output_file,'w')

	#write header
	for sampleID in sample_list:
		output_txt.write("\t%s" % sampleID)
	output_txt.write('\n')

	#write main contents
	write_output_sub(output_txt, feature_dict, feature_list, sample_list)
	output_txt.close()

def write_output_sub(output_txt, feature_dict, feature_list, sample_list):

	for feature in feature_list:
		output_txt.write("%s" % feature)

		for sampleID in sample_list:
			value = feature_dict[sampleID, feature]
			output_txt.write("\t%s" % value)
		output_txt.write("\n")


if __name__ == "__main__":
	print ('This is not meant to be run')

else:
	import pandas as pd
	import numpy as np
	import sys
	import os
	print ("LOADING :: cv_preparation")

