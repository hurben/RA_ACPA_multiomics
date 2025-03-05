#Inherits the code from: enet_construction_preprocess.py        #22.05.10 code reviewed
#designed for metabolites only
#
#[1] Split full data into 5 fold data.
#[2] Further used for template network construction and machine learning.


if __name__ == "__main__":
	import sys
	import os
	import subprocess
	import pandas as pd
	import numpy as np

	import io_management as IOM
	import cv_preperation as CVP

	data_file_location = 'data_locations.txt'
	omics_list = ["metabolites", "patient_info"]

	#skip steps (for various reasons..)
	step1 = 1
	step2 = 1
	step3 = 1
	
	if step1 == 1:
		PI_dict, PI_patient_list, PI_list = IOM.access_data_location(data_file_location,"patient_info")
		M_dict, M_patient_list, M_list  = IOM.access_data_location(data_file_location,"metabolites")
	#Note: patient list from each matrix should be the same
	
	if step2 == 1:
		multiplex_dict, feature_list = CVP.merge_multiple_dict_main_c1p3(PI_dict, M_dict, PI_patient_list, PI_list, M_list)

	if step3 == 1:
		CVP.create_kfold_dataset(multiplex_dict, feature_list, PI_patient_list, 5)
