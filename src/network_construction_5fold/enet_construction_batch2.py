#inherited from "enet_construction.py"       22.05.10
#
#designed to run ElasticNet on 5fold data

if __name__ == "__main__":
	import sys
	import os
	sys.path.insert(1, '../../../src')

	#create result folder
	result_dir = "result"
	if os.path.isdir(result_dir) == False:
		os.system('mkdir %s' % result_dir)
	else:
	#	os.system('rm -r %s' % result_dir)
		os.system('mkdir %s' % result_dir)
	
	data_type = 'multiplex'

	#rotate kfold
	i = 1
	kfold = "%sfold" % (i + 1)
	print ("STAGE: %s" % kfold)
	output_kfold_dir = "%s/%s" % (result_dir, kfold)

	#Make Kfold folder if not exists
	if os.path.isdir(output_kfold_dir) == False:
		os.system('mkdir %s' % output_kfold_dir)

	input_file = "%s/%s.train.tsv" % (kfold, data_type)
	output_file = "%s/%s.enet.tsv" % (output_kfold_dir, data_type)
	
	cmd = "Rscript ../../../src/network_construction_5fold/ElasticNet_R.short.r %s %s" % (input_file, output_file)
	print (cmd)
	os.system(cmd)

else:
	None
