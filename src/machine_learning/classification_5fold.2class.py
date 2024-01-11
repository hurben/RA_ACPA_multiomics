def run_ML(train_df, test_df, specified_classifier, class_type):

	y_train = train_df.iloc[:,0]
	X_train = train_df.iloc[:,1:]

	y_test = test_df.iloc[:,0]
	X_test = test_df.iloc[:,1:]

	clf = specified_classifier
	clf.fit(X_train, y_train)
	y_pred = clf.predict(X_test)

	#summarize prediction results: obtain TPR TNR FPR TNR
	negative_class = class_type.split('_')[0]
	positive_class = class_type.split('_')[1]

	tp_count = 0
	fp_count = 0
	tn_count = 0
	fn_count = 0

	observed_class_list = list(y_test)
	predicted_class_list = list(y_pred)

	for i in range(len(observed_class_list)):
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

def main(fs_data_folder, data_file_name, specified_classifier, threhold, classifier_type, output_txt, class_type):

	performance_dict = {}
	acc_list = []
	pre_list = []
	tpr_list = []
	tnr_list = []
	fpr_list = []
	fnr_list = []
	npv_list = []

	for i in range(5):
		kfold = '%sfold' % (i+1)

		train_data = '%s/%s/%s/%s.fs.train.tsv' % (fs_data_folder,threshold, kfold, data_file_name)
		test_data = '%s/%s/%s/%s.fs.test.tsv' % (fs_data_folder, threshold, kfold, data_file_name)

		train_df = pd.read_csv(train_data, sep='\t', index_col=0, low_memory=False)
		train_df = train_df.T
		test_df = pd.read_csv(test_data, sep='\t', index_col=0, low_memory=False)
		test_df = test_df.T

		acc, pre, tpr, tnr, fpr, fnr, npv = run_ML(train_df, test_df, specified_classifier, class_type)
		acc_list.append(acc)
		pre_list.append(pre)
		tpr_list.append(tpr)
		tnr_list.append(tnr)
		fpr_list.append(fpr)
		fnr_list.append(fnr)
		npv_list.append(npv)
	
	print ("----------")
	print (acc_list)
	print ("----------")

	output_txt.write('%s_%s_%s' % (threshold, data_file_name, classifier_type))
	output_txt.write('\t%s\t%s' % (statistics.mean(acc_list), statistics.stdev(acc_list)))
	output_txt.write('\t%s\t%s' % (statistics.mean(pre_list), statistics.stdev(pre_list)))
	output_txt.write('\t%s\t%s' % (statistics.mean(tpr_list), statistics.stdev(tpr_list)))
	output_txt.write('\t%s\t%s' % (statistics.mean(tnr_list), statistics.stdev(tnr_list)))
	output_txt.write('\t%s\t%s' % (statistics.mean(fpr_list), statistics.stdev(fpr_list)))
	output_txt.write('\t%s\t%s' % (statistics.mean(fnr_list), statistics.stdev(fnr_list)))
	
	try: 
		output_txt.write('\t%s\t%s' % (statistics.mean(npv_list), statistics.stdev(npv_list)))
	except TypeError: 
		output_txt.write('\t%s\t%s' % ((npv_list), (npv_list)))

	output_txt.write('\n')

if __name__ == '__main__':

	import pandas as pd
	import sys

	from sklearn.linear_model import LogisticRegression
	from sklearn.ensemble import RandomForestClassifier
	from sklearn.tree import DecisionTreeClassifier
	from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
	from sklearn.naive_bayes import GaussianNB
	from sklearn.ensemble import AdaBoostClassifier
	from sklearn.neural_network import MLPClassifier
	from sklearn.gaussian_process import GaussianProcessClassifier
	from sklearn.ensemble import GradientBoostingClassifier
	from sklearn.metrics import confusion_matrix
	from sklearn.svm import SVC
	import statistics
	import math
	
	#[1] RWR result file
	#[2] kfold_data_dir='/Users/m221138/RA_multiomics/analysis/10fold_data_v3/network_construction_enet
	#[3] split
	#[4] output folder name

	data_file_name = 'multiplex'

	fs_data_folder = sys.argv[1]
	split_type = sys.argv[2]
	output_file = sys.argv[3]
	class_type = sys.argv[4]

	if split_type == "percentage":
		split_list = ["1p", "5p", "10p", "20p", "25p", "30p", "40p", "50p", "100p"]
	if split_type == "top":
		split_list = ["top10", "top20", "top30", "top40", "top50", "top60", "top70", "top80", "top90", "top100","top200","top300","top400","top500","top600", "top700","top800","top900","top1000"]

	output_txt = open(output_file,'w')

	output_txt.write('Algorithm\tACC_average\tACC_stdev\tPRE_average\tPRE_stdev\tTPR_average\tTPR_stdev\tTNR_average\tTNR_stdev\tFPR_average\tFPR_stdev\tFNR_average\tFNR_stdev\tNPV_average\tNPV_stdev\n')


	for threshold in split_list:

#		print (threshold, 'LR')
#		specified_classifier = LogisticRegression(max_iter=1000, random_state=123)
#		main(fs_data_folder, data_file_name, specified_classifier, threshold, 'LR', output_txt, class_type)

		print (threshold, 'RF')
		specified_classifier = RandomForestClassifier(random_state=123)
		main(fs_data_folder, data_file_name, specified_classifier, threshold, 'RF', output_txt, class_type)

	output_txt.close()
