#RWR.R
#
#Random walk with restart running on default.
#
#Intended inputs: output from (1) cleanup_RWR_ready_file.py, (2) RWR_create_seed_profile.py; which is kfold.topology.v2.tsv, kfold.p0.txt

library("diffusr")

args <- commandArgs(TRUE)

#inputs
adjacency_matrix_file <- args[1]
p0_file <- args[2]
result_file <- args[3]

#load adj matrix
table_file <- read.table(adjacency_matrix_file, header=TRUE, sep="\t")

temp_table <- table_file[,2:ncol(table_file)]
rownames(temp_table) <- table_file[,1]
graph <- as.matrix(temp_table)

#load p0 files (seed_list)
p0_table <- read.table(p0_file, header=FALSE, sep="\t")
p0 <- as.vector(p0_table[,2])

#run RWR
pt <- random.walk(p0, graph)
pt <- pt$p.inf

#output
rownames(pt) <- table_file[,1]

pt_df <- as.data.frame(pt)
pt_df <- pt_df[order(pt[,1], decreasing=TRUE), ,drop=FALSE]

write.table(pt_df, result_file, sep="\t", quote=FALSE, col.names=FALSE)
