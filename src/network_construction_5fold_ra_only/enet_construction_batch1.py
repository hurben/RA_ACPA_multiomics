if __name__ == "__main__":
        import sys
        import os
        sys.path.insert(1, '../../../src')
        seed = sys.argv[1]

        #create result folder
        result_dir = "result"
        if os.path.isdir(result_dir) == False:
            os.system('mkdir %s' % result_dir)
        else:
            os.system('mkdir %s' % result_dir)
        
        data_type = 'multiplex'

        i = 0

        kfold = "%sfold" % (i + 1)
        print ("STAGE: %s" % kfold)
        output_kfold_dir = "%s/%s" % (result_dir, kfold)

        #Make Kfold folder if not exists
        if os.path.isdir(output_kfold_dir) == False:
                os.system('mkdir %s' % output_kfold_dir)

        input_file = "%s/%s.train.tsv" % (kfold, data_type)
        output_file = "%s/%s.enet.tsv" % (output_kfold_dir, data_type)
        
        cmd = "Rscript ../../../src/network_construction_5fold_ra_only/ElasticNet_R.short.r %s %s %s" % (input_file, output_file, seed)
        print (cmd)
        os.system(cmd)

else:
        None
