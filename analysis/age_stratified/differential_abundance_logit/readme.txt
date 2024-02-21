Designed to:
[1] split sample into three group based on age (low-group: bottom 33%, med-group: medium 33%, high-group: high 33%)
[2] perform logistic regression, while feature_abundance is a list of the normalized value of the biomolecular (e.g., one metabolite across all samples).
[2-1] sample_phenotype ~ feature_abundance + sex + age + BMI + smoking_history + prednisone + bDMARDs + csDMARDS
[3] perform Cohen's D to obtain the effect size from [2]
