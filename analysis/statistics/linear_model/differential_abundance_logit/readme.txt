Identifying disease-associated features:

[1] Perform logistic regression models while adjusting for sex, age, BMI, smoking history, prednisone use, and use of bDMARDs and csDMARDs.
[1-1] sample_phenotype ~ feature_abundance + sex + age + BMI + smoking_history + prednisone + bDMARDs + csDMARDS
[2] perform Cohen's D to obtain the effect size
