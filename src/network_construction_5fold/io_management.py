#io_management.py			
#
#Designed to be called by [enet_construction_preprocess.py]
# - parses information from patient dataprofile

def access_data_location(data_location_file, file_type):

	data_location_df = pd.read_csv(data_location_file, sep = "\t", header=None)
	r, c = data_location_df.shape

	for i in range(r):

		data_type = data_location_df.iloc[i][0]
		data_dir = data_location_df.iloc[i][1]

		if data_type == file_type:

			if file_type == "patient_info":
				patient_dict, patient_list, patient_variable_list = load_patient_data(data_dir)
				return patient_dict, patient_list, patient_variable_list

			if file_type == "metabolites" or file_type == "autoantibody" or file_type == "proteomics":
				feature_dict, patient_list, feature_list = load_general_df_data(data_dir, file_type)
				return feature_dict, patient_list, feature_list

def load_patient_data(data_dir):

	data_df = pd.read_csv(data_dir, sep="\t", index_col=0)
	r, c = data_df.shape

	patient_dict = {}
	patient_list = []
	patient_variable_list = list(data_df.index.values)
	patient_list = list(data_df.columns.values)

	for i in range(r):
		feature = patient_variable_list[i]

		for j in range(c):
			patientID = patient_list[j]
			value = data_df.iloc[i][j]

			patient_dict[patientID, feature] = value

	return patient_dict, patient_list, patient_variable_list

def load_general_df_data(data_dir, file_type):
#Designed for plasma metabolite, immune profile, 

	data_df = pd.read_csv(data_dir, sep="\t")
	r, c = data_df.shape

	patient_list = data_df.columns.values[1:]
	feature_dict = {}
	feature_list = []

	for i in range(r):
		feature = data_df.iloc[i][0]
		feature_list.append(feature)

		for j in range(1,c):
			value = data_df.iloc[i][j]

			try: value = value.replace(',', '')
			except AttributeError: None

			patientID = patient_list[j-1]

			feature_dict[patientID, feature] = value

	return feature_dict, patient_list, feature_list


if __name__ == "__main__":
	print ('This is not meant to be run')
else:
	import pandas as pd
	import numpy as np
	import math
	print ("LOADING :: io_management")
