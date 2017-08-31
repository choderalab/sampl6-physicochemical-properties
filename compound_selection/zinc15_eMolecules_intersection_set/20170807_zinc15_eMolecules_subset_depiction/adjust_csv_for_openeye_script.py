# Creates a csv file with organized columns to create an input for csv2xlsx.py

import pandas as pd

# Read df
df =  pd.read_csv("df_frag_final.csv")

# Reorder columns names to have first column canonical isomeric smiles column
cols = list(df.columns.values)
print(cols)
adj_cols = [cols[2],cols[1]]
#print("")

for column in iter(cols[3:]):
    adj_cols.append(column)

# add canonical isomeric smiles column to last
adj_cols.append(cols[2])
adj_cols.append(cols[1])
# print(adj_cols)

# Reorder dataframe according to adjusted column name order
df = df[adj_cols]

# Rename 1st canonical isomeric smiles column as "SMILES"
df.columns.values[0] = "SMILES"

# Write to csv without index column
df.to_csv("df_frag_final_oe.csv", index = False)
print(df)
