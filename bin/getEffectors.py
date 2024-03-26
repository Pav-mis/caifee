import pandas as pd
import sys
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_table(sys.argv[1], header = None, delimiter="\t").dropna(axis=0)
species_filtered_df = df[df[1].str.contains(sys.argv[2])]
similarity_filtered_df = species_filtered_df[species_filtered_df[3]==100.00]
similarity_filtered_df = similarity_filtered_df[similarity_filtered_df[2]==0.0]
similarity_filtered_df = similarity_filtered_df.drop_duplicates(subset=[0], keep="first")
similarity_filtered_df = similarity_filtered_df.drop(columns=[2,3])
similarity_filtered_df[0] = similarity_filtered_df[0].str.split('|').str[-1]
similarity_filtered_df[1] = similarity_filtered_df[1].str.split('#').str[-1]

similarity_filtered_df.to_csv(sys.argv[3]+".tsv", sep = "\t", header=False, index=False)
    