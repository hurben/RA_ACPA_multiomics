for i in 20
do
	echo $i
	seed_directory=seed_$i
	if [ -d "$seed_directory" ]; then
		rm -r "$seed_directory"
		mkdir "$seed_directory"
	else
		mkdir "$seed_directory"
	fi
	python ../../../src/revision/machine_learning_handle_imbalanced/classification_N_summary.ver_external.py neg_vs_pos $seed_directory $i
done
