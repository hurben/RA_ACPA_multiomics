#ElasticNet_R_PI
#PI: Patient Information as dependent variable
#Currently designed for 
#das28crp
#cdai

library(glmnet)
library(dplyr)
library(caret)
library(stringr)

args <- commandArgs(trailingOnly=TRUE)
data_file = args[1]
output_txt = args[2]

set.seed(123)

#output related
if (file.exists(output_txt)) {
  file.remove(output_txt)
}

print (data_file)
data_df = read.csv(data_file, sep = "\t", row.names=1)
data_df = data_df[!rownames(data_df) %in% "acpa", ]
data_df = t(data_df)

row_length = nrow(data_df)
col_length = ncol(data_df)
feature_list = colnames(data_df)

#MAIN 
feature_size = length(feature_list)
output_df = data.frame(matrix(ncol= feature_size, nrow = feature_size))
colnames(output_df) <- feature_list
rownames(output_df) <- feature_list

for (i in 1:col_length)
{
    #For each feature as Y
    feature = feature_list[i]
	y_df = data_df[,i]
	x_df = data_df[,-i]

	process_stage = i%%1000
	if (process_stage == 0){
		print(paste(i, '/', col_length,sep=''))
	}

	#calculate ENet of Y ~ others 
	train_control = trainControl(method = "cv",
					number = 10)
	
	#Error will be caused due to all "zero" features
	tryCatch(
		{
			elastic_net_model = train(y= y_df, x= x_df, 
									  method = "glmnet",
									  tuneLength = 10,
									  trControl = train_control)

			#Summarize output
			#coefficients <- coef(elastic_net_model$finalModel, elastic_net_model$bestTune$lambda)
			coefficients <- coef(elastic_net_model$finalModel, s = elastic_net_model$bestTune$lambda, alpha = elastic_net_model$bestTune$alpha)
			coefficient_feature_list = rownames(coefficients)

			for (i in 1:length(coefficient_feature_list))
			{
				coefficient_feature = coefficient_feature_list[i]
				coefficient_feature_value = coefficients[i]

				if (feature != coefficient_feature)
				{
					if (coefficient_feature != "(Intercept)")
					{
						output_df[feature, coefficient_feature] = coefficient_feature_value
						#row = feature, column = coefficient_feature
					}
				}
			}
		}, 
		error= function(e)
		{ 
			print (paste("Attention to: ", feature, sep=""))
		}
	)

}
#write.csv(output_df, output_txt, sep="\t", row.names = TRUE, quote=FALSE)
write.table(output_df, output_txt, sep="\t", row.names = TRUE, quote=FALSE)


