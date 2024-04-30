def ML_performance(y_test, y_pred):
    #summarize prediction results: obtain TPR TNR FPR TNR
    negative_class = 1
    positive_class = 2

    tp_count = 0
    fp_count = 0
    tn_count = 0
    fn_count = 0
    all_count = 0

    observed_class_list = list(y_test)
    predicted_class_list = list(y_pred)

    for i in range(len(observed_class_list)):
        all_count += 1
        observed_value = observed_class_list[i]
        predicted_value = predicted_class_list[i]

        if observed_value == positive_class:
            if predicted_value == positive_class: #Truely RA
                tp_count += 1
            if predicted_value == negative_class: #
                fn_count += 1

        if observed_value == negative_class:
            if predicted_value == negative_class:
                tn_count += 1
            if predicted_value == positive_class:
                fp_count += 1

    try:
        acc = (tp_count + tn_count) / (tp_count + fp_count + tn_count + fn_count)
        pre = (tp_count) / (tp_count + fp_count)
        tpr = (tp_count) / (tp_count + fn_count)
        tnr = (tn_count) / (tn_count + fp_count)
        fpr = (fp_count) / (fp_count + tn_count)
        fnr = (fn_count) / (fn_count + tp_count)
        
        try: npv = (tn_count) / (tn_count + fn_count)
        except ZeroDivisionError: npv = "nan"

    except ZeroDivisionError:
        print ("Error ACC: %s %s %s %s" % (tp_count, tn_count, fp_count, tn_count, fn_count))
        print (observed_class_list)
        print (predicted_class_list)
    
    return acc, pre, tpr, tnr, fpr, fnr, npv

if __name__ == "__main__":

	import pandas as pd
	import numpy as np
	import sys
	import os

	from sklearn.ensemble import RandomForestClassifier
	from sklearn.utils import resample

	import statistics
	import math

	input_file = sys.argv[1] 
	output_dir = sys.argv[2]
	seed = sys.argv[3]

	output_txt = open("%s/ml_summary.tsv" % output_dir,'w')
	#output_txt.write('Algorithm\tcutoff\tACC\tPRE\tTPR\tTNR\tFPR\tFNR\tNPV\n')
	output_txt.write('Algorithm\tcutoff\tACC_average\tACC_stdev\tPRE_average\tPRE_stdev')
	output_txt.write('\tTPR_average\tTPR_stdev\tTNR_average\tTNR_stdev\tFPR_average\tFPR_stdev')
	output_txt.write('\tFNR_average\tFNR_stdev\tNPV_average\tNPV_stdev\n')

#	split_type_dict = {"percentage": ["1p", "5p", "10p", "20p", "25p", "30p", "40p", "50p", "100p"],
#						"top": ["top10", "top20", "top30", "top40", "top50", "top60", "top70", "top80", "top90", "top100","top200","top300","top400","top500","top600", "top700","top800","top900","top1000"]}
	split_type_dict = {"top": ["top10", "top20", "top30", "top40", "top50", "top60", "top70", "top80", "top90", "top100","top200","top300","top400","top500","top600", "top700","top800","top900","top1000"]}

	for split_type in list(split_type_dict.keys()):
		split_list = split_type_dict[split_type]

		for feature_size in split_list:
			print ("Cutoff: %s" % feature_size)
			os.system("mkdir %s/%s" % (output_dir, feature_size)) 

			if split_type == "percentage":
				data_file = '%s/%s/full_metabolomics.fs.train.tsv' % (input_file, feature_size)
			else:
				data_file = '%s/%s/full_metabolomics.fs.train.tsv' % (input_file, feature_size)

			data_df = pd.read_csv(data_file, sep="\t", index_col = 0)
			data_df = data_df.T
			r, c = data_df.shape

			X_train = data_df.drop('acpa', axis=1)  # Features
			y_train = data_df['acpa']  # Labels

			clf = RandomForestClassifier(random_state=int(seed))
			clf.fit(X_train, y_train)

			if split_type == "percentage":
				test_data_file = '%s/%s/full_metabolomics.fs.test.scaled.tsv' % (input_file, feature_size)
			else:
				test_data_file = '%s/%s/full_metabolomics.fs.test.scaled.tsv' % (input_file, feature_size)

			test_data_df = pd.read_csv(test_data_file, sep="\t", index_col = 0)
			test_data_df = test_data_df.T

			df_majority = test_data_df[test_data_df.acpa == 1]
			df_minority = test_data_df[test_data_df.acpa == 2]

			# Downsample majority class
			resample_acc_list = []
			resample_pre_list = []
			resample_tpr_list = []
			resample_tnr_list = []
			resample_fpr_list = []
			resample_fnr_list = []
			resample_npv_list = []

			for j in range(1000):
				df_majority_downsampled = resample(df_majority, 
												   replace=False,     # sample without replacement
												   n_samples=len(df_minority),  # to match minority class
												   random_state=123 + j)  # reproducible results

				# Combine minority class with downsampled majority class
				df_balanced = pd.concat([df_majority_downsampled, df_minority])

				# Shuffling data
				df_balanced = df_balanced.sample(frac=1, random_state=123 + j).reset_index(drop=True)
				df_balanced.to_csv("%s/%s/%s.balanced.test.tsv" % (output_dir, feature_size, j), sep="\t", index=False)

				# Separating features and labels for the balanced dataset
				X_test_balanced = df_balanced.drop('acpa', axis=1)
				y_test_balanced = df_balanced['acpa']

				class_counts = df_balanced['acpa'].value_counts()
				y_pred = clf.predict(X_test_balanced)

				acc, pre, tpr, tnr, fpr, fnr, npv = ML_performance(y_test_balanced, y_pred)
				resample_acc_list.append(acc)
				resample_pre_list.append(pre)
				resample_tpr_list.append(tpr)
				resample_tnr_list.append(tnr)
				resample_fpr_list.append(fpr)
				resample_fnr_list.append(fnr)
				resample_npv_list.append(npv)

			print (resample_acc_list)
			output_txt.write('RF\t%s(common:%s)' % (feature_size, c-1))
			output_txt.write('\t%s\t%s' % (statistics.mean(resample_acc_list), statistics.stdev(resample_acc_list)))
			output_txt.write('\t%s\t%s' % (statistics.mean(resample_pre_list), statistics.stdev(resample_pre_list)))
			output_txt.write('\t%s\t%s' % (statistics.mean(resample_tpr_list), statistics.stdev(resample_tpr_list)))
			output_txt.write('\t%s\t%s' % (statistics.mean(resample_tnr_list), statistics.stdev(resample_tnr_list)))
			output_txt.write('\t%s\t%s' % (statistics.mean(resample_fpr_list), statistics.stdev(resample_fpr_list)))
			output_txt.write('\t%s\t%s' % (statistics.mean(resample_fnr_list), statistics.stdev(resample_fnr_list)))
			output_txt.write('\t%s\t%s' % (statistics.mean(resample_npv_list), statistics.stdev(resample_npv_list)))
			output_txt.write('\n')

	output_txt.close()
