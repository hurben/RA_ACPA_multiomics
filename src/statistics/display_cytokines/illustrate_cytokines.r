#illustrate_cytokines.R
#
#two tasks:

#task 1: draw cytokine condition significance heatmap.
#[1] get all sig cytokine list
#[2] merge into a single list
#[3] color code (up, down, not sig)

#task 2: draw heatmap based on 'abundances'. However, will need context of conditions.

library(pheatmap)
library(ggplot2)

change_dbl_to_category <- function(x) {
  ifelse(x > 0, "UP", ifelse(x < 0, "DOWN", "None"))
}

#Task 1:

#buffer
input_file = "../../../analysis/statistics/cytokine_boxplots/all_adj_cytokine_df_v2.tsv"
input_df = read.csv(input_file, sep="\t", row.names=1)

acpa_values <- as.numeric(input_df[1, ])
sorted_order <- order(acpa_values)
input_df <- input_df[ , sorted_order]

sample_info_df = input_df[rownames(input_df) == "acpa", ]
sample_info_df = t(sample_info_df)

cytokine_annotation_file = "../../../analysis/statistics/cytokine_boxplots/cytokine_annoation.tsv"
cytokine_annotation_df = read.csv(cytokine_annotation_file, sep="\t")
cytokine_list = cytokine_annotation_df[,1]

input_df <- input_df[rownames(input_df) %in% cytokine_list, ]
input_df <- input_df[match(cytokine_list, rownames(input_df)), ]

annotation_df <- data.frame(
    cytokine = cytokine_list,   # Use cytokine_list as row names
    cohenD_cVSneg = NA,             
    cohenD_cVSpos = NA,    
    cohenD_negVSpos = NA
)
rownames(annotation_df) = annotation_df$cytokine

#get input 
condition_list <- c("cVSneg","cVSpos","negVSpos")
for (condition in condition_list){
    print (condition)
    data_file = paste("../../../analysis/statistics/linear_model/differential_abundance_logit/proteomics.", condition, ".tsv", sep="")
    data_df = read.csv(data_file, sep="\t")

    filtered_df <- data_df[data_df[, 1] %in% cytokine_list, ]
    row.names(filtered_df) <- NULL

    for (i in length(filtered_df)){
        for (i in 1:nrow(filtered_df)){
        
            cytokine_name <- filtered_df[i,1]
            pval <- filtered_df$all_adj_pval[i]
            cohenD <- filtered_df$cohenD[i]
            if (pval < 0.05 && abs(cohenD) > 0.2){

                if (condition == "cVSneg"){
                    annotation_df$cohenD_cVSneg[annotation_df$cytokine == cytokine_name] <- cohenD
                }
                if (condition == "cVSpos"){
                    annotation_df$cohenD_cVSpos[annotation_df$cytokine == cytokine_name] <- cohenD
                }                
                if (condition == "negVSpos"){
                    annotation_df$cohenD_negVSpos[annotation_df$cytokine == cytokine_name] <- cohenD
                }
                
            } else{
                if (condition == "cVSneg"){
                    annotation_df$cohenD_cVSneg[annotation_df$cytokine == cytokine_name] <- 0
                }
                if (condition == "cVSpos"){
                    annotation_df$cohenD_cVSpos[annotation_df$cytokine == cytokine_name] <- 0
                }                
                if (condition == "negVSpos"){
                    annotation_df$cohenD_negVSpos[annotation_df$cytokine == cytokine_name] <- 0
                }
            }
        }    
    }
}

columns_to_update <- c("cohenD_cVSneg", "cohenD_cVSpos", "cohenD_negVSpos")
annotation_df[columns_to_update] <- lapply(annotation_df[columns_to_update], change_dbl_to_category)
annotation_df = subset(annotation_df, select= -cytokine)

ann_colors <- list(
    cohenD_cVSneg = c('UP' = "firebrick4", 'DOWN' = "darkolivegreen3", 'None' = 'snow2'),
    cohenD_cVSpos = c('UP' = "firebrick4", 'DOWN' = "darkolivegreen3", 'None' = 'snow2'),
    cohenD_negVSpos = c('UP' = "firebrick4", 'DOWN' = "darkolivegreen3", 'None' = 'snow2'),
    acpa = c("0" = "#78AF3F", "1" = "#636363", "2" = "#B57623")
)

my_colors <- colorRampPalette(c("steelblue", "snow2", "red4"))(30)
breaks <- seq(-1, 1, length.out = 31)  # 51 for 50 intervals between colors

# Convert the matrix to a data frame
sample_info_df <- as.data.frame(sample_info_df)

# Optional: Set the row names using the first column (if appropriate)
rownames(sample_info_df) <- rownames(sample_info_df)
sample_info_df$acpa <- as.factor(sample_info_df$acpa)

pdf("../../../analysis/statistics/cytokine_boxplots/all_adj_cytokine_df.pdf", width = 20, height = 10)
gt <- pheatmap(input_df,
        scale="row",
        cluster_cols = FALSE,
        cluster_rows = TRUE,
        annotation_row = annotation_df,
        annotation_colors = ann_colors,
        annotation_col = sample_info_df,
        color = my_colors, 
        breaks = breaks,
        cellwidth = 8,
        cellheight = 20,
        show_colnames = FALSE,  # Remove column labels
        )
print (gt)
dev.off()

# pdf("../../../analysis/statistics/cytokine_boxplots/all_adj_cytokine_df.pdf", width = 20, height = 10)
# gt <- pheatmap(input_df,
#          scale="row",
#          cluster_cols = FALSE,
#          cluster_rows = FALSE,
#          annotation_row = annotation_df,
#          annotation_colors = ann_colors,
#          annotation_col = sample_info_df,
#          color = my_colors, 
#          breaks = breaks,
#         cellwidth = 8,
#         cellheight = 20,
#          show_colnames = FALSE,  # Remove column labels
#         )$gtable
# ggsave("../../../analysis/statistics/cytokine_boxplots/all_adj_cytokine_df.pdf", plot=gt, width = 20, height = 10)


