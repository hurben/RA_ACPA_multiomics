top1 ~ top 50 (positive corrleation)
top1 ~ top 50 (negative corrleation)

Designed to be runned with scripts from src/statistics/omics_clinical_feature_correlation

Note: If the script is runned by deidentified sample matrix, the script needs edit on specific function:

make_correlation_dict()

from 
LINE51: value = data_dict[feature, str(int(patientID))]

to
LINE51: value = data_dict[feature, str(patientID)]

This is because original patient ID was in number's not with strings like "temp1"
