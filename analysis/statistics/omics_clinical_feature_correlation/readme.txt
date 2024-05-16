top1 ~ top 50 (positive corrleation)
top1 ~ top 50 (negative corrleation)

Designed to be runned with scripts from src/statistics/omics_clinical_feature_correlation

Note: If the script is runned by deidentified sample matrix, the script needs edit on specific function:

Script: /src/statistics/omics_clinical_feature_correlation/PREPROCESS_make_omics_correlation_matrix_top_bottom_50_v3.ipynb
Function:
make_correlation_dict()

LINE51: 
from
value = data_dict[feature, str(int(patientID))]
to
value = data_dict[feature, str(patientID)]

This is because original patient ID was in number's not with strings like "temp1"
