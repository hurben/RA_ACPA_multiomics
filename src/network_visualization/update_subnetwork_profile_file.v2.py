#update_subnetwork_profile_file.v2.py			22.04.25
#
#make a fc profile from subnetwork						22.04.25
# -> which can be done by "find_subnetwork_from_cyto_file.py"
#
#[1] Parse edge information from "full_data_subnetwork.profile.tsv"
#[2] add average abundance to "full_data_subnetwork.profile.tsv" and save as "full_data_subnetwork.profile.v2.tsv"

#output file contains 
#node, rank, control average, acpa neg average, acpa pos average, ra average
#---------------------------------------------------------------------------

#make profile dict
def make_target_feature_dict(data_file):

	data_dict = {}
	target_feature_list = []

	data_df = pd.read_csv(data_file, sep="\t")
	r, c = data_df.shape

	for i in range(r):
		feature = data_df.iloc[i][0]
		rank = data_df.iloc[i][1]

		if feature != 'acpa':
			data_dict[feature, "rank"] = rank
			target_feature_list.append(feature)

	target_feature_list = list(set(target_feature_list))

	return data_dict, target_feature_list

#get patient info
def make_patient_info_file_dict(data_file):

	data_dict = {}

	data_df = pd.read_csv(data_file, sep="\t")
	r, c = data_df.shape

	for i in range(r):
		patientID = data_df["sample_ID"][i]
		acpa = data_df["acpa"][i]

		data_dict[patientID] = acpa

	return data_dict

#make omics dict; if the feature is in profile dict.
def make_omics_dict(data_file, patient_info_dict, target_feature_list, feature_profile_dict, omics_type):

	data_df = pd.read_csv(data_file, sep="\t", index_col=0)
	data_patientID_list = data_df.columns.values
	data_feature_list = data_df.index.values
	r, c = data_df.shape

	for i in range(r):
		feature = data_feature_list[i]

		if omics_type == "aa":
			feature = '%s_%s' % (omics_type, feature)
		if omics_type == "p":
			feature = '%s_%s' % (omics_type, feature)
			feature = feature.replace('-','_')
		if omics_type == "m":
			feature = feature.replace("'",'prime')
			feature = feature.replace('-','_')
			feature = feature.replace(' ','_')
			feature = feature.replace(',','_')

		if feature in target_feature_list:
			control_value_list = []
			acpa_pos_value_list = []
			acpa_neg_value_list = []
			ra_value_list = []

			for j in range(c):
				value = data_df.iloc[i][j]
				patientID = int(data_patientID_list[j])
				acpa = patient_info_dict[patientID]

				if acpa == 0:
					control_value_list.append(value)
				if acpa == 1:
					acpa_pos_value_list.append(value)
					ra_value_list.append(value)
				if acpa == 2:
					acpa_neg_value_list.append(value)
					ra_value_list.append(value)

			feature_profile_dict[feature, "control"] = control_value_list
			feature_profile_dict[feature, "acpa_pos"] = acpa_pos_value_list
			feature_profile_dict[feature, "acpa_neg"] = acpa_neg_value_list
			feature_profile_dict[feature, "ra"] = ra_value_list

	return feature_profile_dict

def make_deg_dict(deg_dict, data_file, omics_type, comparison_type):

	data_df = pd.read_csv(data_file, sep="\t", index_col=0)
	data_feature_list = data_df.index.values
	r, c = data_df.shape

	for i in range(r):
		feature = data_feature_list[i]

		if omics_type == "aa":
			feature = '%s_%s' % (omics_type, feature)
		if omics_type == "p":
			feature = '%s_%s' % (omics_type, feature)
			feature = feature.replace('-','_')
		if omics_type == "m":
			feature = feature.replace("'",'prime')
			feature = feature.replace('-','_')
			feature = feature.replace(' ','_')
			feature = feature.replace(',','_')

		pval = data_df["pval"][i]

		if omics_type == "aa":
			if pval < 0.05:
				deg_dict[feature, comparison_type] = pval
		if omics_type == "p" or omics_type == "m":
			if pval < 0.01:
				deg_dict[feature, comparison_type] = pval

	return deg_dict


def make_output_file(feature_profile_dict, target_feature_list, deg_dict, output_file):

	output_txt = open(output_file, 'w')
	output_txt.write('feature\trank\tcontrol\tacpa_pos\tacpa_neg\tra\tlog2fc_cVSra\tlog2fc_cVSpos\tlog2fc_cVSneg\t')
	output_txt.write('cVSra_is_deg\tcVSpos_is_deg\tcVSneg_is_deg\tnode_type\n')
	index_list = ['rank','control','acpa_pos','acpa_neg','ra']
	condition_list = ['cVSra','cVSneg','cVSpos']

	for feature in target_feature_list:
		
		if 'p_' in feature:
			output_txt.write(feature.split('_')[1])
		else:
			output_txt.write(feature)

		for index in index_list:
			value = feature_profile_dict[feature,index]

			if index != 'rank':
				value = statistics.mean(value)
			output_txt.write('\t%s' % value)
		#fc (ra/control)
		output_txt.write('\t%s' % math.log2(statistics.mean(feature_profile_dict[feature,'ra']) / statistics.mean(feature_profile_dict[feature,'control'])))

		#fc (acpa+/control)
		output_txt.write('\t%s' % math.log2(statistics.mean(feature_profile_dict[feature,'acpa_pos']) / statistics.mean(feature_profile_dict[feature,'control'])))

		#fc (acpa-/control)
		output_txt.write('\t%s' % math.log2(statistics.mean(feature_profile_dict[feature,'acpa_neg']) / statistics.mean(feature_profile_dict[feature,'control'])))


		for condition in condition_list:
			value = 0
			try: 
				pval = deg_dict[feature, condition]
				if pval < 0.01:
					value = 1
			except KeyError:
				None
			output_txt.write('\t%s' % value)

		node_type = 0
		if 'p_' in feature:
			node_type = 1
		if 'aa_' in feature:
			node_type = 2
		output_txt.write('\t%s' % node_type)

		output_txt.write('\n')

	output_txt.close()


if __name__ == "__main__":

	import sys
	import pandas as pd
	import statistics
	import math

	subnetwork_profile_file = sys.argv[1]
	output_file = '%s.v2.tsv' % subnetwork_profile_file.split('.tsv')[0]

	patient_info_file = '../../../preprocessed_data/meta/patient_info_for_statistics.tsv'

	p_data_file = '../../../preprocessed_data/proteomics/somascan_anml.T.v2.tsv'
	m_data_file = '../../../preprocessed_data/metabolomics/metabolone_raw_norm_preprocessed.v2.tsv'
	aa_data_file = '../../../preprocessed_data/autoantibody/sengenics_qnorm_data.v2.tsv'

	feature_profile_dict, target_feature_list = make_target_feature_dict(subnetwork_profile_file)
	patient_info_dict = make_patient_info_file_dict(patient_info_file)

	feature_profile_dict = make_omics_dict(p_data_file, patient_info_dict, target_feature_list, feature_profile_dict, 'p')
	feature_profile_dict = make_omics_dict(m_data_file, patient_info_dict, target_feature_list, feature_profile_dict, 'm')
	feature_profile_dict = make_omics_dict(aa_data_file, patient_info_dict, target_feature_list, feature_profile_dict, 'aa')

	deg_dict = {}

	deg_data_dir = '../../../analysis/statistics/linear_model/differential_abundance'
	condition_list = ['cVSra','cVSpos','cVSneg']
	omics_list = ['metabolomics','proteomics']

	for omics_data in omics_list:
		for condition_type in condition_list:
			deg_data_file = '%s/%s.%s.padj.v2.med.tsv' % (deg_data_dir, omics_data, condition_type)

			if omics_data == 'autoantibody':
				omics_type = 'aa'
			if omics_data == 'metabolomics':
				omics_type = 'm'
			if omics_data == 'proteomics':
				omics_type = 'p'
			deg_dict = make_deg_dict(deg_dict, deg_data_file, omics_type, condition_type)


	make_output_file(feature_profile_dict, target_feature_list, deg_dict, output_file)
	
