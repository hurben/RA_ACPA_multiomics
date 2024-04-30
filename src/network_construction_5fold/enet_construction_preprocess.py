create_kfold_dataset
#enet_construction_preprocess.py		#22.05.10 code reviewed 
#
#[1] Split full data into 5 fold data.
#[2] Further used for template network constructio and machine learning.

if __name__ == "__main__":
	import sys
	import os
	import subprocess
	import pandas as pd
	import numpy as np

	import io_management as IOM
	import cv_preperation as CVP

	data_file_location = 'data_locations.txt'
	omics_list = ["proteomics", "autoantibody","metabolites","patient_info"]

	#skip steps (Debug option)
	step1 = 1
	step2 = 1
	step3 = 1
	
	#get data information (sample info, matrix_info)
	if step1 == 1:
		PI_dict, PI_patient_list, PI_list = IOM.access_data_location(data_file_location,"patient_info")
		M_dict, M_patient_list, M_list  = IOM.access_data_location(data_file_location,"metabolites")
		AA_dict, AA_patient_list, AA_list = IOM.access_data_location(data_file_location, "autoantibody")
		P_dict, P_patient_list, P_list = IOM.access_data_location(data_file_location, "proteomics")
	#Note: patient list from each matrix should be the same
	
	common_sample_list = list(set(PI_patient_list) & set(M_patient_list) & set(AA_patient_list) & set(P_patient_list))

	#make a single multiplex dataframe
	if step2 == 1:
		multiplex_dict, feature_list = CVP.merge_multiple_dict_main(PI_dict, M_dict, AA_dict, P_dict, PI_patient_list, PI_list, M_list, AA_list, P_list)

	#split that multiplex dataframe into 5fold data
	if step3 == 1:
		CVP.create_kfold_dataset(multiplex_dict, feature_list, PI_patient_list, 5)
