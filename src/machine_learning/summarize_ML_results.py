#"summarize_ML_results.py"			22.04.04 -> 24.01.11

def main(defined_condition_list, comparison_list, output_file):

	summary_dict = {}

	feature_selection_list = ['topN', 'percentage']

	for feature_selection in feature_selection_list:
		for condition_folder in defined_condition_list:
		
			omics_type = get_omics_info(condition_folder)

			for comparison in comparison_list:

				if feature_selection == 'percentage':
					ml_result_file = '%s/classification.result.%s.enet.tsv' % (condition_folder, comparison)
				else:
					ml_result_file = '%s/classification.%s.result.%s.enet.tsv' % (condition_folder, feature_selection, comparison)

				summary_dict = update_summary_dict(ml_result_file, summary_dict, omics_type, comparison)
	
	make_output(summary_dict, output_file)


def update_summary_dict(ml_result_file, summary_dict, omics_type, comparison):

	open_file = open(ml_result_file, 'r')
	file_readlines = open_file.readlines()

	for i in range(1, len(file_readlines)):
		read = file_readlines[i]
		read = read.replace('\n', '')
		token = read.split('\t')

		data_classifier_type = token[0]
		omics_data_classifier_type = '%s_%s_%s' % (omics_type, data_classifier_type, comparison)

		for j in range(1, len(token)):
			value = token[j]
			try: summary_dict[omics_data_classifier_type].append(value)
			except KeyError: summary_dict[omics_data_classifier_type] = [value]

	open_file.close()

	#note: summary dict save information in order of:
	#ACC_average, ACC_stdev, PRE_average, PRE_stdev, TPR_average, TPR_stdev, TNR_average, TNR_stdev, FPR_average, FPR_stdev, FNR_average, FNR_stdev, NPV_average,NPV_stdev

	return summary_dict


def get_omics_info(condition_folder):

	condition_info_dict = {"enet_1condition_p1": "1omics_p",
							"enet_1condition_p2": "1omics_aa",
							"enet_1condition_p3":"1omics_m",
							"enet_2condition_p1":"2omics_pa",
							"enet_2condition_p2":"2omics_pm",
							"enet_2condition_p3":"2omics_am",
							"enet_3condition":"3omics_pam"}

#	condition_info_dict = {"enet_3condition":"3omics_PAM"}

	condition_info_dict = {"enet_1condition_p1": "1omics_p",
							"enet_1condition_p2": "1omics_aa",
							"enet_1condition_p3":"1omics_m",
							"enet_3condition":"3omics_pam"}

	omics_info = condition_info_dict[condition_folder]

	return omics_info

def make_output(summary_dict, output_file):
	
	output_txt = open(output_file,'w')
	#write header
	#output_txt.write('Algorithm')
	output_txt.write("omics_type\tomics_data\tthrshold\tdata_structure\tclassifier\tclassification_task")

	output_txt.write('\tACCURACY_average\tACCURACY_stdev\tPRECISION_average\tPRECISION_stdev\tTPR_average\tTPR_stdev\tTNR_average\tTNR_stdev\tFPR_average\tFPR_stdev\tFNR_average\tFNR_stdev\tNPV_average\tNPV_stdev\n')

	#write content
	for ml_test_key in list(summary_dict.keys()):

		algorithm_info_list = ml_test_key.split("_")
		output_txt.write(algorithm_info_list[0])

		for i in range(1, len(algorithm_info_list)):
			output_txt.write("\t%s" % algorithm_info_list[i])

		#note summary dict:
		#ACC_average, ACC_stdev, PRE_average, PRE_stdev, TPR_average, TPR_stdev, TNR_average, TNR_stdev, FPR_average, FPR_stdev, FNR_average, FNR_stdev, NPV_average,NPV_stdev
		for performance in summary_dict[ml_test_key]:
			output_txt.write('\t%s' % performance)
		output_txt.write('\n')
		
	output_txt.close()


if __name__ == "__main__":
	
	import sys
	import pandas as pd

	#this list is fixed purpose.
	#defined_condition_list = ["enet_1condition_p1","enet_1condition_p2","enet_1condition_p3","enet_2condition_p1", "enet_2condition_p2", "enet_2condition_p3","enet_3condition"]
	defined_condition_list = ["enet_1condition_p1","enet_1condition_p2","enet_1condition_p3","enet_3condition"]
	#defined_condition_list = ["enet_3condition"]

	#comparison_list = ["cVSneg","cVSpos","cVSra","posVSneg"]
	comparison_list = ["cVSneg","cVSpos", "cVSra"]

	output_file = sys.argv[1]
	main(defined_condition_list, comparison_list, output_file)
	
