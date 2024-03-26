import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

import sys

genes = pd.read_table(sys.argv[1], delimiter='\t', header=None).dropna(axis=0)
genes.columns = ['gene_name', 'cai', 'phenotype']
genes = genes.drop(columns=['gene_name'])
non_effectors = genes[genes['phenotype'] == 'gene']
effectors = genes[genes['phenotype'] != 'gene']
print(effectors)
plt.figure(figsize=(10, 10), dpi=200)
sns.violinplot(data=non_effectors, y='cai', cut=0, color="#A7C7E7")
sns.swarmplot(data=effectors, y='cai', hue='phenotype', s=5)



plt.savefig(sys.argv[1]+'.png')

