import pandas as pd
import sys
import numpy as np

cai = pd.read_table(sys.argv[1], header = None, delimiter=' ').dropna(axis=0)
cai = cai.drop(columns=[0,2])
cai.columns = ['gene_name', 'cai']
effectors = pd.read_table(sys.argv[2], delimiter='\t', header = None).dropna(axis=0)
effectors.columns = ['gene_name', 'phenotype']

merged_df = pd.merge(cai, effectors, on=['gene_name'], how='left')
merged_df['phenotype'].fillna('gene', inplace=True)

merged_df.to_csv(sys.argv[1]+".tsv", sep = "\t", header=False, index=False)