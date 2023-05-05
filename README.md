# Integrative Multi-omic Phenotyping in Blood Identifies Molecular Signatures and Candidate Biomarkers of ACPA-negative Rheumatoid Arthritis

DOI: TBD

Authors: Benjamin Hur, Minsik Oh, Vinod K. Gupta, Kevin Y. Cunningham, Kerry A. Wright, Hu Zeng, Elena Myasoedova, Cynthia S. Crowson, Kenneth Warrington, John M. Davis, and Jaeyun Sung

## Omics data preprocess

#### 1. Preprocess: Proteomics data from Somascan's delivered file (i.e., .adat)

> src/preprocess/PREPROCESS_somascan_raw_data_STEP1.ipynb
> src/preprocess/PREPROCESS_somascan_raw_data_STEP2.ipynb

```
Designed to:
1. remove non-human proteins (e.g., Spurimoer, Spurimer)
2. address duplicated proteins (but aptamer is targeting different site)
3. & other minor things to make multi-omics comparison feasble (e.g., unifying sample ID)
```


#### 2. Preprocess: Metabolomics data from Metabolon's delivered file (i.e., DATA TABLE.XLSX, Batch-normalized Data)



3.


