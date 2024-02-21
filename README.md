Integrative Multi-omic Phenotyping in Blood Identifies Molecular Signatures and Candidate Biomarkers of ACPA-negative Rheumatoid Arthritis

DOI: TBD

Authors: Benjamin Hur, Minsik Oh, Vinod K. Gupta, Kevin Y. Cunningham, Hu Zeng, Cynthia S. Crowson, Kenneth J. Warrington, Elena Myasoedova, Vanessa L. Kronzer, John M. Davis, and Jaeyun Sung

## Overview

![plot](./etc/Figure1_v3.png)

```
[A] Deep plasma multi-omic profiling was utilized to create a dataset comprising 9,944 proteins, metabolites, and autoantibodies from 40 ACPA– RA patients, 40 ACPA+ RA patients, and 40 healthy controls. 
```

```
[B] Statistical analyses and set comparisons were performed to characterize and differentiate the three study cohorts at the single- and multi-omic levels. 
A multi-omic network that elucidates associations between various omic features and clinical attributes, including study group (or phenotype), was constructed using penalized (elastic net) linear regression. 
```

```
[C] The feature selection scheme for phenotype classification between study groups is composed of three main steps: 
i) Multi-omic network construction: Nodes represent omic features, and edges symbolize links between features inferred using elastic net linear regression. This step forms the backbone of the network, laying the groundwork for subsequent analyses. 
ii) Network topology propagation via random walker algorithm: Initiated from a seed node representing the clinical phenotype (i.e., ACPA– RA, ACPA+ RA, or controls), this process aims to identify omic features most closely connected to phenotypes on the network topology. The random walker algorithm, specifically a random walk with restart, refines the initial full network into a smaller sub-network composed of features most closely linked to phenotypes. 
iii) Evaluation in 5-fold cross-validation: A random forest classifier was trained on the identified omic features to evaluate their potential for phenotype classification.
```

## Omics data preprocess

Note: Preprocessed files are shared in this URL: [URL HERE]
#### 1. Preprocess: Proteomics data from Somascan's delivered file (i.e., .adat)

> src/preprocess/proteomics/PREPROCESS_somascan_raw_data_STEP1.ipynb
> src/preprocess/proteomics/PREPROCESS_somascan_raw_data_STEP2.ipynb

```
Designed to:
[1] remove non-human proteins (e.g., Spurimoer, Spurimer)
[2] address duplicated proteins (aptamer is targeting different site)
[3] & other minor things to make multi-omics comparison feasble (e.g., unifying sample ID)
```

#### 2. Preprocess: Metabolomics data from Metabolon's delivered file (i.e., DATA TABLE.XLSX, Batch-normalized Data)

> src/preprocess/metabolomics/01_PREPROCESS_metabolon_raw_data_STEP1.ipynb
> src/preprocess/metabolomics/02_PREPROCESS_metabolon_raw_data_STEP2.ipynb
> src/preprocess/metabolomics/03_PREPROCESS_metabolon_raw_data_STEP3.ipynb

```
Designed to:
[1] remove metabolites that have more than 20% of N/A values (across all samples)
[2] after [1], follow the same normalization method that Metabolon performs (i.e., each metabolite is re-scaled to have median 1)
[3] after [2], imput missing value of with the metabolite's minimum value across all samples. For example, if 2 was the minimum value of metaboliteX across 10 samples. missing value will be imputed as 2.
[4] & other minor things to make multi-omics comparison feasble (e.g., unifying sample ID)
```

#### 3. Preprocess: Autoantibody data from Sengenic's delivered file (i.e., KREX Immunome.xlsx, Raw Mean)

>src/preprocess/autoantibody/01_PREPROCESS_sengenics_quantile_norm_STEP1.ipynb
>src/preprocess/autoantibody/02_PREPROCESS_sengenics_quantile_norm_STEP2.ipynb

```
Designed to:
[1] quantile normalize the data
[2] & other minor things to make multi-omics comparison feasble (e.g., unifying sample ID)
```

#### 4. Preprocess: merging three different multi-omics matrix and patient information into a single matrix

>src/preprocess/multiomics/PREPROCESS_make_3_omics_matrix.py.ipynb

```
Designed to:
[1] merge preprocessed proteomics, metabolomics, autoantibody, and patient information data into single matrix
[2] handle some feature names that Rscript cannot handle.
```

## Statistics

#### 1. Organize demographics and perform statistics for clinical variables (e.g., treatment, sex, age) (Manuscript Table. 1)

>src/statistics/patient_info/summarize_demographics_for_table1.ipynb
>src/statistics/patient_info/table1_statistics.ipynb

```
Designed to:
[1] use input data from: preprocessed_data/meta/patient_info_for_statistics.tsv, preprocessed_data/meta/patient_info_for_statistics.v3.tsv
[2] use Fisher's Exact Test, Kruskal-Wallis rank sum test was used to measure statistics.
```

#### 2. Create a ternary plot to compare the properties of the profiled plasma multi-omics data. (Manscript Fig. 2A)

>src/statistics/ternary_plots/STEP01_PREPROCESS_Ternary_Plot.ipynb
>src/statistics/ternary_plots/STEP02_Ternary_Plot.ipynb

```
Designed to:
[1] create a ternary plot for each proteomics, metabolomics, and autoantibody profiles
[2] store results at: analysis/statistics/ternary_plots/
```

#### 3. Create a scatter plot of correlations between clinical marker and omics-feature; and to compare 'rho' values of ACPA-negative RA-specific samples and ACPA-positive RA-specific samples. (Manuscript Fig. 2B)

>src/statistics/omics_clinical_feature_correlation/PREPROCESS_make_omics_correlation_matrix_top_bottom_50_v3.ipynb
>src/statistics/omics_clinical_feature_correlation/draw_scatterplots_for_figure2_v2.ipynb

```
Designed to:
[1] create a scatter plots of correlations between clinical variable (e.g., ESR) and omics-feature.
[2] visualize only top 50 (positive correlation) and top 50 (negative correlation) 
[3] store results at: analysis/statistics/omics_clinical_feature_correlation
```

#### 4. Linear regression & Cohen's D to identify phenotype-associated proteins/metabolites/autoantibodies (Manuscript Fig. 3A, 3C)

>src/statistics/linear_model_logit/01_DifferentialAbundance_and_cohens_D_adjust_effect.ipynb
>src/statistics/linear_model_logit/02_report_differential_abundance_adjusting_drug.ipynb

>src/statistics/volcano_plots/MAKE_volcano_plot_Rscript.ipynb
>src/statistics/volcano_plots/PREPROCESS_identify_cytokines_from_significant_proteins.ipynb
>src/statistics/boxplot_for_cytokines/DRAW_boxplots_for_7_cytokines.ipynb

```
Designed to:
[1] Perform logistic regression models while adjusting for sex, age, BMI, smoking history, prednisone use, and use of bDMARDs and csDMARDs. 
[1-1] sample_phenotype ~ feature_abundance + sex + age + BMI + smoking_history + prednisone + bDMARDs + csDMARDS
[2] perform Cohen's D to obtain the effect size
[3] visualize identified features using volcano plots
[4] visualize differentiall abundant cytokines
```

#### 5. Metabolomic analysis with age-stratified samples (Manuscript Fig. 4D)

>src/age_stratified_differences/linear_model_logit/00_split_into_three_age_group_v3.ipynb
>src/age_stratified_differences/linear_model_logit/01_DifferentialAbundance_and_cohens_D_v2.ipynb

```
Designed to:
[1] split sample into three group based on age (low-group: bottom 33%, med-group: medium 33%, high-group: high 33%)
[2] perform logistic regression, while feature_abundance is a list of the normalized value of the biomolecular (e.g., one metabolite across all samples).
[2-1] sample_phenotype ~ feature_abundance + sex + age + BMI + smoking_history + prednisone + bDMARDs + csDMARDS
[3] perform Cohen's D to obtain the effect size from [2]
```

#### 6. Inverted correlation network (Manuscript Fig. 5)

Note: Requires long-computations. Processed files are shared in this URL: [URL HERE]

>analysis/correlation_network/topology_data/01_make_condition_specific_network.sh
>analysis/correlation_network/topology_data/pbs.batch*.sh
>analysis/correlation_network/topology_data/pbs.padj.batch*.sh
>analysis/correlation_network/topology_data/02_get_sig_network.sh
>analysis/correlation_network/topology_data/03_get_sig_network_posneg.sh

>analysis/correlation_network/network_similarity/01_network_similarity.sh
>analysis/correlation_network/network_similarity/02_make_cytocape_ready_format.sh
```
Designed to:
[1] infer a correlation (all pair-wise feature associations) network from condition-specific datasets (i.e., ACPA-negative RA specific, ACPA-positive RA specific)
[2] "edges" are defined by BH-adjusted P < 0.05, |rho| > 4
[3] find network edges that are completely the opposite (if the edge is positive-rho in ACPA-negative RA and negative-rho in ACPA-positive RA, this is considered inversed)

*PBS scripts have been run in cluster that has different directory structure. Please note that the directory might need to be adjusted.

Shell scripts utlizes
>src/correlation_network/STEP0_condition_specific_correlation.py
>src/correlation_network/STEP1_make_sigNcorr_results_v2.py
>src/correlation_network/STEP2_update_topology_pad.py
>src/correlation_network/STEP3_topology_with_threshold.py (currently, I am not using this script)
>src/correlation_network/STEP3_topology_with_threshold_ver_rho_split.py
>src/correlation_network/STEP4_analyze_network_similary.py
>src/correlation_network/STEP5_make_cytoscape_ready_format_v3.py
```

## Machine-learning

Note: Requires long-computations. Processed files are shared in this URL: [URL HERE]
#### 1. create 5-fold dataset

>analysis/5fold_data/network_construction_enet/01_preprocess_omics_enet.sh
```
Split dataset into balanced (each K-fold dataset contains an equal amount of classes) 5-fold dataset.

The shell script utilizes
>src/network_construction_5fold/enet_construction_preprocess.py
```

#### 2. infer a network from 5-fold dataset (using elastic net)

>analysis/5fold_data/network_construction_enet/02_create_omics_enet.*.sh
```
For each K-fold dataset, perform elastic net to 

The shell script utilizes
>src/network_construction_5fold/enet_construction_batch1.py
```

#### 3. infer a network from 5-fold dataset (using elastic net)

>analysis/post_network_enet/5fold/enet_3condition/01_organize_topology_files.sh
```
Make adjacent matrix into topology (source-target).
The shell script utlizes
>src/post_network/integrate_network.v2.py
```

>analysis/post_network_enet/5fold/enet_3condition/02_preprocess_RWR.sh
```
RWR script (from R) has problem understanding some strings. This scripts tries to avoid those issues.

The shell script utilizes
>src/post_network/cleanup_RWR_ready_file.py
```

>analysis/post_network_enet/5fold/enet_3condition/03_make_RWR_p0.sh
```
Prepare for RWR 'seed' list.
The shell script utlizes
>src/post_network/RWR_create_seed_profile.py
```

>analysis/post_network_enet/5fold/enet_3condition/04_run_RWR.sh
```
Run RWR

The shell script utlizes
>src/post_network/RWR.R
```

#### 4. Perform machine-learning

>analysis/machine_learning/5fold_v2/enet_3condition/01_create_feature_selected_matrix.sh
>analysis/machine_learning/5fold_v2/enet_3condition/02_create_feature_selected_matrix.v2.sh
```
Prepare matrices for machine leanring. Each matrix will contain selective-features from elasticnet and various cutoff thresholds

The shell script utlizes
>src/machine_learning/create_feature_selection_matrix.py
```

>analysis/machine_learning/5fold_v2/enet_3condition/03_3class_to_2class.sh
>analysis/machine_learning/5fold_v2/enet_3condition/04_do_classification.sh
>analysis/machine_learning/5fold_v2/enet_3condition/05_3class_to_2class.sh
>analysis/machine_learning/5fold_v2/enet_3condition/06_do_classification.sh

```
[1] prepare the data for two-class classification. For example, if the machine-learning task is for ACPA-negative vs. control, discard ACPA-positive class samples from the data.
[2] perform machine-learning with feature-seleted matrices.

The shell script ultilzes 
>src/machine_learning/transform_3class_to_2class_matrix.py
>src/machine_learning/classification_5fold.2class.py
```

>analysis/machine_learning/5fold_v2/summarize_ML_results.py

```
Designed to summarize ML results from /analysis/machine_learning/5fold_v2
```


## Misc

#### Addressing Reviewer comments


#### Machine learning processed data

Data that has been generated during the 5fold-CV process can be seen here:
```
URL:
```
