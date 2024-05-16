# Integrative Multi-omic Phenotyping in Blood Identifies Molecular Signatures and Candidate Biomarkers of ACPA-negative Rheumatoid Arthritis

**DOI:** TBD

**Authors:** Benjamin Hur, Minsik Oh, Vinod K. Gupta, Kevin Y. Cunningham, Hu Zeng, Cynthia S. Crowson, Kenneth J. Warrington, Elena Myasoedova, Vanessa L. Kronzer, John M. Davis, and Jaeyun Sung

## Overview

![plot](./etc/Figure1_v3.png)

### [A] Deep plasma multi-omic profiling

Utilized to create a dataset comprising 9,944 proteins, metabolites, and autoantibodies from:
- 40 ACPA– RA patients
- 40 ACPA+ RA patients
- 40 healthy controls

### [B] Statistical analyses and set comparisons

Performed to characterize and differentiate the three study cohorts at the single- and multi-omic levels. A multi-omic network that elucidates associations between various omic features and clinical attributes, including study group (or phenotype), was constructed using penalized (elastic net) linear regression.

### [C] Feature selection scheme for phenotype classification

Composed of three main steps:
1. **Multi-omic Network Construction:** Nodes represent omic features, and edges symbolize links between features inferred using elastic net linear regression.
2. **Network Topology Propagation via Random Walker Algorithm:** Initiated from a seed node representing the clinical phenotype (i.e., ACPA– RA, ACPA+ RA, or controls), this process aims to identify omic features most closely connected to phenotypes on the network topology.
3. **Evaluation in 5-fold Cross-validation:** A random forest classifier was trained on the identified omic features to evaluate their potential for phenotype classification.

## Omics Data Preprocess

> **NOTE:** Preprocessed files are stored in "preprocessed_data_public". Please rename "preprocessed_data_public" to "preprocessed_data" if you wish to reproduce the study results.

### 1. Preprocess: proteomics data from Somascan's delivered File (.adat)

- `src/preprocess/proteomics/PREPROCESS_somascan_raw_data_STEP1.ipynb`
- `src/preprocess/proteomics/PREPROCESS_somascan_raw_data_STEP2.ipynb`

Designed to:
1. Remove non-human proteins.
2. Address duplicated proteins.
3. Unify sample IDs for multi-omics comparison.

### 2. Preprocess: metabolomics data from Metabolon's delivered File (DATA TABLE.XLSX, Batch-normalized Data)

- `src/preprocess/metabolomics/01_PREPROCESS_metabolon_raw_data_STEP1.ipynb`
- `src/preprocess/metabolomics/02_PREPROCESS_metabolon_raw_data_STEP2.ipynb`
- `src/preprocess/metabolomics/03_PREPROCESS_metabolon_raw_data_STEP3.ipynb`

Designed to:
1. Remove metabolites with >20% N/A values (across all samples).
2. Normalize metabolites to median 1.
3. Impute missing values with the metabolite's minimum value.
4. Unify sample IDs for multi-omics comparison.

### 3. Preprocess: autoantibody data from Sengenic's delivered file (KREX Immunome.xlsx, raw mean)

- `src/preprocess/autoantibody/01_PREPROCESS_sengenics_quantile_norm_STEP1.ipynb`
- `src/preprocess/autoantibody/02_PREPROCESS_sengenics_quantile_norm_STEP2.ipynb`

Designed to:
1. Quantile normalize the data.
2. Unify sample IDs for multi-omics comparison.

### 4. Preprocess: merging multi-omics matrices and patient information into a single matrix

- `src/preprocess/multiomics/PREPROCESS_make_3_omics_matrix.py.ipynb`

Designed to:
1. Merge preprocessed proteomics, metabolomics, autoantibody, and patient information data into a single matrix.
2. Handle feature names that Rscript cannot process.

## Statistics

### 1. Organize demographics and perform statistics for clinical variables (Manuscript Table 1)

- `src/statistics/patient_info/summarize_demographics_for_table1.ipynb`
- `src/statistics/patient_info/table1_statistics.ipynb`

Designed to:
1. Use input data from: `preprocessed_data/meta/patient_info_for_statistics.tsv`, `preprocessed_data/meta/patient_info_for_statistics.v3.tsv`.
2. Apply Fisher's Exact Test and Kruskal-Wallis rank sum test for statistics.

### 2. Create a ternary plot to compare properties of the profiled plasma multi-omics data (Manuscript Fig. 2A)

- `src/statistics/ternary_plots/STEP01_PREPROCESS_Ternary_Plot.ipynb`
- `src/statistics/ternary_plots/STEP02_Ternary_Plot.ipynb`

Designed to:
1. Create a ternary plot for proteomics, metabolomics, and autoantibody profiles.
2. Store results at: `analysis/statistics/ternary_plots/`.

### 3. Create scatter plot of correlations between clinical markers and omics features (Manuscript Fig. 2B)

- `src/statistics/omics_clinical_feature_correlation/PREPROCESS_make_omics_correlation_matrix_top_bottom_50_v3.ipynb`
- `src/statistics/omics_clinical_feature_correlation/draw_scatterplots_for_figure2_v2.ipynb`

Designed to:
1. Create scatter plots of correlations between clinical variables (e.g., ESR) and omics features.
2. Visualize the top 50 positive and top 50 negative correlations.
3. Store results at: `analysis/statistics/omics_clinical_feature_correlation/`.

### 4. Linear regression & Cohen's D to identify phenotype-associated proteins/metabolites/autoantibodies (Manuscript Fig. 3A, 3B, 4A, 4B, 5A, 5B)

- `src/statistics/linear_model_logit/01_DifferentialAbundance_and_cohens_D_adjust_effect.ipynb`
- `src/statistics/linear_model_logit/02_report_differential_abundance_adjusting_drug.ipynb`
- `src/statistics/volcano_plots/MAKE_volcano_plot_Rscript.ipynb`
- `src/statistics/volcano_plots/PREPROCESS_identify_cytokines_from_significant_proteins.ipynb`
- `src/statistics/boxplot_for_cytokines/DRAW_boxplots_for_7_cytokines.ipynb`

Designed to:
1. Perform logistic regression models while adjusting for various factors.
2. Obtain effect size using Cohen's D.
3. Visualize identified features using volcano plots and differential cytokines.

### 5. Metabolomic analysis with age-stratified samples (Manuscript Fig. 4D)

- `src/age_stratified_differences/linear_model_logit/00_split_into_three_age_group_v3.ipynb`
- `src/age_stratified_differences/linear_model_logit/01_DifferentialAbundance_and_cohens_D_v2.ipynb`

Designed to:
1. Split samples into three age groups.
2. Perform logistic regression and Cohen's D analysis.

### 6. Autoantibody correlation with clinical parameters (Manuscript Fig. 5C–D)

- `src/statistics/autoantibody_correlation/PREPROCESS01_make_correlation_ready_profile_v2.ipynb`
- `src/statistics/autoantibody_correlation/PREPROCESS02_make_correlation_ready_profile.ipynb`
- `src/statistics/autoantibody_correlation/PREPROCESS03_make_correlation_ready_profile.ver_binary.V2.ipynb`
- `src/statistics/autoantibody_correlation/PREPROCESS04_make_correlation_ready_profile_V2.ipynb`
- `src/statistics/autoantibody_correlation/draw_heatmap_correlation_v2.ipynb`

Designed to:
Calculate Spearman’s rank correlation coefficient (ρ) between plasma autoantibodies and clinical parameters. Only significant correlations (|ρ| > 0.4 and P < 0.01) are represented in the heatmap.

### 7. Inverted correlation network (Manuscript Fig. 6)

- `analysis/correlation_network/topology_data/01_make_condition_specific_network.sh`
- `analysis/correlation_network/topology_data/pbs.batch*.sh`
- `analysis/correlation_network/topology_data/pbs.padj.batch*.sh`
- `analysis/correlation_network/topology_data/02_get_sig_network.sh`
- `analysis/correlation_network/topology_data/03_get_sig_network_posneg.sh`
- `analysis/correlation_network/network_similarity/01_network_similarity.sh`
- `analysis/correlation_network/network_similarity/02_make_cytocape_ready_format.sh`

Designed to:
1. Infer a correlation network from condition-specific datasets.
2. Define "edges" by BH-adjusted P < 0.05 and |rho| > 4.
3. Identify inverted network edges. <br />
**Note**: PBS scripts have been run in a cluster with a different directory structure; adjustments may be necessary.

```
Shell scripts utlizes
>src/correlation_network/STEP0_condition_specific_correlation.py
>src/correlation_network/STEP1_make_sigNcorr_results_v2.py
>src/correlation_network/STEP2_update_topology_pad.py
>src/correlation_network/STEP3_topology_with_threshold.py (currently, I am not using this script)
>src/correlation_network/STEP3_topology_with_threshold_ver_rho_split.py
>src/correlation_network/STEP4_analyze_network_similary.py
>src/correlation_network/STEP5_make_cytoscape_ready_format_v3.py
```


## Machine Learning

### 1. Create 5-fold dataset

- `analysis/5fold_data/network_construction_enet/01_preprocess_omics_enet.sh`
- `analysis/5fold_data_ra_only/network_construction_enet/01_preprocess_omics_enet.sh`

Designed to: split datasets into balanced 5-fold datasets.

```
The shell script utilizes
>src/network_construction_5fold/enet_construction_preprocess.py
>src/acpa_specific_network_construction_5fold/enet_construction_preprocess.py
```

### 2. Infer a network from 5-fold dataset using elastic net (Part 1)

For each K-fold dataset, perform elastic net to infer network from the data.
Due to running time, I've splitted the data into several batches and runned via cluster.

- `analysis/5fold_data/network_construction_enet/02_create_omics_enet.*.sh`
- `analysis/5fold_data_ra_only/network_construction_enet/02_create_omics_enet.*.sh`

**NOTE:** Elastic net results are stored in:
- [5fold_data results](https://drive.google.com/drive/folders/1GRRf2O6ZrstjEWVxZUrdSMM96oJjRcIL)
- [5fold_data_ra_only results](https://drive.google.com/drive/folders/1N0EH0RBowVidHv-6JZHl5hmmpL-5Db9d)
- Please use these files for down-stream analysis if you wish to reproduce the study results.

```
The shell script utilizes
>src/network_construction_5fold/enet_construction_batch*.py
>src/network_construction_5fold_ra_only/enet_construction_batch*.py

enet_construction_batch*.py utilizes
>src/src/network_construction_5fold/ElasticNet_R.short.r
>src/src/network_construction_5fold_ra_only/ElasticNet_R.short.r
```

### 3. Infer a network from 5-fold dataset using elastic net (Part 2)

#### 3.1 Make adjacent matrix into topology (source-target).

- `analysis/post_network_enet/5fold/enet_3condition/01_organize_topology_files.sh`
- `analysis/post_network_enet_ra_only/5fold/enet_3condition/01_organize_topology_files.sh`


**NOTE:** RWR results are stored in:
- [5fold_data results](https://drive.google.com/drive/folders/140W1aTweCnttRaEUKgpsrA6Z3Y_T_8Do)
- [5fold_data_ra_only results](https://drive.google.com/drive/folders/1JZhhVDHIZlCwRGMzJgUdu5MOFoak1STc)
- RWR results were performed with the output from elastic net results provided in the step mentioned above.

```
The shell script utilizes
>src/post_network/integrate_network.v2.py
```

#### 3.2 RWR script (from R) has problem understanding some strings. This scripts tries to avoid those issues.
- `analysis/post_network_enet/5fold/enet_3condition/02_preprocess_RWR.sh`
- `analysis/post_network_enet_ra_only/5fold/enet_3condition/02_preprocess_RWR.sh`

```
The shell script utilizes
>src/post_network/cleanup_RWR_ready_file.py
```

#### 3.3  Prepare for RWR 'seed' list.

- `analysis/post_network_enet/5fold/enet_3condition/03_make_RWR_p0.sh`
- `analysis/post_network_enet_ra_only/5fold/enet_3condition/03_make_RWR_p0.sh`

```
The shell script utlizes
>src/post_network/RWR_create_seed_profile.py
```

#### 3.4 Run RWR

- `analysis/post_network_enet/5fold/enet_3condition/04_run_RWR.sh`
- `analysis/post_network_enet_ra_only/5fold/enet_3condition/04_run_RWR.sh`

```
The shell script utlizes
>src/post_network/RWR.R
```

### 4. Perform Machine Learning

#### 4.1 Prepare matrices for machine learning with features selected by elasticnet and RWR cutoff thresholds.

Results are stored in `Table S23.xlsx` in the manuscript.

- `analysis/machine_learning/5fold_v2/enet_3condition/01_create_feature_selected_matrix.sh`
- `analysis/machine_learning/5fold_v2/enet_3condition/02_create_feature_selected_matrix.v2.sh`
- `analysis/machine_learning_ra_only/enet_3condition/01_create_feature_selected_matrix.sh`
- `analysis/machine_learning_ra_only/enet_3condition/02_create_feature_selected_matrix.v2.sh`

```
01_create_feature_selected_matrix.sh is for applying RWR cutoffs via percentage (e.g., top1%, top 5%)
01_create_feature_selected_matrix.v2.sh is for applying RWR cutoffs via top N (e.g., top10, top 20)

The shell script utlizes
>src/machine_learning/create_feature_selection_matrix.py
```

Prepare the data for two-class classification. For example, if the machine-learning task is for ACPA-negative vs. control, discard ACPA-positive class samples from the data.

Perform machine-learning with feature-seleted matrices. I highly recommend to read "run.sh" before performing ML.

- `analysis/machine_learning/5fold_v2/enet_3condition/03_3class_to_2class.sh`
- `analysis/machine_learning/5fold_v2/enet_3condition/05_3class_to_2class.sh`
- `analysis/machine_learning/5fold_v2/run.sh`
- `analysis/machine_learning_ra_only/enet_3condition/03_3class_to_2class.sh`
- `analysis/machine_learning_ra_only/run.sh`

```
The shell script ultilzes
>src/machine_learning/transform_3class_to_2class_matrix.py
>src/machine_learning/classification_5fold.2class.opti.withMCC.py
```


### Summarize ML Results

- `src/machine_learning/ML_summary_overall_performance_v2.ipynb`
- `src/machine_learning/ML_summary_overall_performance_v2.negVSpos.ipynb`

Designed to summarize results from:
- `analysis/machine_learning/5fold_v2`
- `analysis/machine_learning_ra_only`

## Misc

### 1. Addressing Reviewer Comments

Not available at the moment.

### 2. Metabolomics Hypergeometric Tests

- `src/statistics/geneset_enrichment/metabolomics/STEP01_PREPROCESS_make_updownDEG.ipynb`
- `src/statistics/geneset_enrichment/metabolomics/STEP02_PREPROCESS_hypergeometric_test_for_metabolomics.ipynb`
- `src/statistics/geneset_enrichment/metabolomics/STEP03_hypergeomteric_test_for_metabolites.ipynb`
- `src/statistics/geneset_enrichment/metabolomics/STEP04_prepare_bubble_plot_format_V2.ipynb`
- `src/statistics/geneset_enrichment/metabolomics/STEP05_draw_bubble_plot_V2.ipynb`

Designed to identify enriched biochemical pathways. Results are stored in `analysis/statistics/gse/metabolomics`.

### 3. Network Inference and RWR with Full Data (Fig 7)

**NOTE:** Elastic net results for 'full_data' are stored in:
- [full_data results](https://drive.google.com/drive/folders/1LCpDAd9GB0mwqqSI-zJ07yTYt1DglwTB)

- `analysis/full_data/create_omics_enet.sh`
- `analysis/full_data/post_network_enet/01_organize_topology_files.sh`
- `analysis/full_data/post_network_enet/02_preprocess_RWR.sh`
- `analysis/full_data/post_network_enet/03_make_RWR_p0.sh`
- `analysis/full_data/post_network_enet/04_run_RWR.sh`
- `analysis/full_data/cytoscape_top30/01_make_cytoscape_ready_from_full_topology.sh`
- `analysis/full_data/cytoscape_top30/02_subnetwork_from_full_topology.sh`

Designed to infer the network on full data and perform RWR.

```
Shell script utilizes:
src/network_construction_5fold/ElasticNet_R.short.fulldata.r
src/post_network/integrate_network.v2.py
src/post_network/cleanup_RWR_ready_file.py
src/post_network/RWR_create_seed_profile.py
src/post_network/RWR.R
src/network_visualization/make_cytoscape_ready_file.py
src/network_visualization/find_subnetwork_from_cyto_file.py
```

### 4. External Validation of Machine Learning

External validation was performed on ACPA– vs. ACPA+ metabolomics; ART and EAC data. The features were used to create a RF classifier while features not in the external validation dataset were discarded.

#### 4-1 Infer Network from Metabolomics Data (RA Only)

Maintains the same philosophy from "Network inference and RWR with full data".

- `analysis/full_data_metabolomics_neg_pos/create_omics_enet.sh`
- `analysis/full_data_metabolomics_neg_pos/post_network_enet/01_organize_topology_files.sh`
- `analysis/full_data_metabolomics_neg_pos/post_network_enet/02_preprocess_RWR.sh`
- `analysis/full_data_metabolomics_neg_pos/post_network_enet/03_make_RWR_p0.sh`
- `analysis/full_data_metabolomics_neg_pos/post_network_enet/04_run_RWR.sh`

**NOTE:** Elastic net results for 'full_data_metabolomics' are stored in: [full_data results](https://drive.google.com/drive/folders/1vFbfahJRDJlJr_CumqcqKhMt_BFRDMMh)

#### 4-2 Data Preprocessing for ART Data

Preprocess the raw peaks using the same principle from our internal validation dataset.

- `src/revision/ART_preprocess/01_PREPROCESS_RA_ART_metabolomics.ipynb`

Prepare feature-selected matrix while discarding features not in the external validation dataset.

- `src/revision/ART_preprocess/02_PREPROCESS_ML_external_validation.ipynb`

#### 4-3 Data Preprocessing for EAC Data

**Note:** This data is unpublished raw dataset. Please contact the corresponding author for data. We will share the data for reasonable requests.

Preprocess the raw peaks using the same principle from our internal validation dataset.

- `src/revision/EAC_preprocess/PREPROCESS_metabolon_raw_data.ipynb`

Prepare feature-selected matrix while discarding features not in the external validation dataset.

- `src/revision/EAC_preprocess/Perform_FS_for_ML_external_validation.ipynb`

#### 4-4 Perform ML

Perform ML on external validation dataset. The script also handles imbalanced classes of the external validation set.

- `analysis_revision/external_validation/ra_art_metabolomics/run.sh`
- `analysis_revision/external_validation/ra_eac_metabolomics/run.sh`

`run.sh` utilizes:
- `src/revision/machine_learning_handle_imbalanced/classification_N_summary.ver_external.v2.py`

### Version

Python packages were last tested with:

**networkx**: 3.3
**scikit-learn**: 1.4.2
**scipy**: 1.13.0

R packages were last tested with:

**lme4**: 1.1-35.1
**dplyr**: 1.1.4
**effects**: 4.2-2
**stringr**: 1.5.1  
**lmerTest**: 3.1-3
**Matrix**: 1.5-4.1 
**effsize**: 0.8.1 
