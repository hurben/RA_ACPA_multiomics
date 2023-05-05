# Integrative Multi-omic Phenotyping in Blood Identifies Molecular Signatures and Candidate Biomarkers of ACPA-negative Rheumatoid Arthritis

DOI: TBD

Authors: Benjamin Hur, Minsik Oh, Vinod K. Gupta, Kevin Y. Cunningham, Kerry A. Wright, Hu Zeng, Elena Myasoedova, Cynthia S. Crowson, Kenneth Warrington, John M. Davis, and Jaeyun Sung

## Omics data preprocess

#### 1. Preprocess: Proteomics data from Somascan's delivered file (i.e., .adat)

> src/preprocess/proteomics/PREPROCESS_somascan_raw_data_STEP1.ipynb
> src/preprocess/proteomics/PREPROCESS_somascan_raw_data_STEP2.ipynb

```
Designed to:
[1] remove non-human proteins (e.g., Spurimoer, Spurimer)
[2] address duplicated proteins (but aptamer is targeting different site)
[3] & other minor things to make multi-omics comparison feasble (e.g., unifying sample ID)
```

#### 2. Preprocess: Metabolomics data from Metabolon's delivered file (i.e., DATA TABLE.XLSX, Batch-normalized Data)

> src/preprocess/metabolomics/01_PREPROCESS_metabolon_raw_data_STEP1.ipynb
> src/preprocess/metabolomics/02_PREPROCESS_metabolon_raw_data_STEP2.ipynb
> src/preprocess/metabolomics/03_PREPROCESS_metabolon_raw_data_STEP3.ipynb

```
Designed to:
[1] remove metabolites have more than 20% of N/A values (across all samples)
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

#### Estimate whether clinical variables (e.g., treatment, sex, age, bmi) influence significantly to the omics-data profile.

>src/statistics/patient_info/demographics_statistics-PERMANOVA.ipynb

```
Designed to:
[1] use input data of 3omics data with all clinical variables
[2] use PERMANOVA (adonis2) with default option

```

### Create a ternary plot to compare the properties of the profiled plasma multi-omics data. (Manscript Fig. 2A)

>src/statistics/ternary_plots/STEP01_PREPROCESS_Ternary_Plot.ipynb
>src/statistics/ternary_plots/STEP02_Ternary_Plot.ipynb

```
Designed to:
[1] create a ternary plot for each proteomics, metabolomics, and autoantibody profiles
[2] store results at: analysis/statistics/ternary_plots/
```

### Create a scatter plot of correlations between clinical marker and omics-feature; and to compare 'rho' values of ACPA-negative RA-specific samples and ACPA-positive RA-specific samples. (Manuscript Fig. 2B)

>src/statistics/omics_clinical_feature_correlation/PREPROCESS_make_omics_correlation_matrix_top_bottom_50_v3.ipynb
>src/statistics/omics_clinical_feature_correlation/draw_scatterplots_for_figure2_v2.ipynb

```
Designed to:
[1] create a scatter plots of correlations between clinical variable (e.g., ESR) and omics-feature.
[2] visualize only top 50 (positive correlation) and top 50 (negative correlation) 
[3] store results at: analysis/statistics/omics_clinical_feature_correlation
```
