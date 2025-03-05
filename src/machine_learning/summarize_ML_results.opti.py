 #"summarize_ML_results.py"			22.04.04    -> 24.04.16

def main(defined_condition_list, comparison_list, output_file, seed):

	summary_dict = {}

	feature_selection_list = ['topN', 'percentage']

	for feature_selection in feature_selection_list:
		for condition_folder in defined_condition_list:
		
			omics_type = get_omics_info(condition_folder)

			for comparison in comparison_list:

				if feature_selection == 'percentage':
					ml_result_file = '%s/%s/classification.result.%s.enet.tsv' % (seed, condition_folder, comparison)
				else:
					ml_result_file = '%s/%s/classification.%s.result.%s.enet.tsv' % (seed, condition_folder, feature_selection, comparison)

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

	return summary_dict


def get_omics_info(condition_folder):

	condition_info_dict = {"enet_2condition":"2omics_PM",
							"enet_1condition_p1": "1omics_P",
							"enet_1condition_p3":"1omics_M"}

	omics_info = condition_info_dict[condition_folder]

	return omics_info

def make_output(summary_dict, output_file):
	
	output_txt = open(output_file,'w')

	#write header
	#output_txt.write('Algorithm\tACCURACY_average\tACCURACY_stdev\tPRECISION_average\tPRECISION_stdev\tTPR_average\tTPR_stdev\tTNR_average\tTNR_stdev\tFPR_average\tFPR_stdev\tFNR_average\tFNR_stdev\tNPV_average\tNPV_stdev\tMCC_average\tMCC_stdev\tF1_average\tF1_stdev\n')
	output_txt.write('Algorithm\tACCURACY_average\tACCURACY_stdev\tPRECISION_average\tPRECISION_stdev\tTPR_average\tTPR_stdev\tTNR_average\tTNR_stdev\tFPR_average\tFPR_stdev\tFNR_average\tFNR_stdev\tNPV_average\tNPV_stdev\tMCC_average\tMCC_stdev\tF1_average\tF1_stdev\tAUC_average\tAUC_stdev\n')

	#write content
	for ml_test_key in list(summary_dict.keys()):
		output_txt.write(ml_test_key)
		for performance in summary_dict[ml_test_key]:
			output_txt.write('\t%s' % performance)
		output_txt.write('\n')
		
	output_txt.close()


if __name__ == "__main__":
	
	import sys
	import pandas as pd

	#this list is fixed purpose.
	defined_condition_list = ["enet_2condition", "enet_1condition_p1", "enet_1condition_p3"]

	comparison_list = ["cVSneg","cVSpos", "cVSra"]
#	comparison_list = ["posVSneg"]

	output_file = sys.argv[1]
	seed = sys.argv[2]
	main(defined_condition_list, comparison_list, output_file, seed)
	
