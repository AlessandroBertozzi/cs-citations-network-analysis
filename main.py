import pandas as pd

df = pd.read_csv('data/1.csv')

print(df['Count_Citing_In_List'].max())
print(df['Count_Cited_In_List'].max())
print(df['Count_Cited_Not_In_List'].max())
print(df['Count_Citing_Not_In_List'].max())
print(df['Is_In_List'].max())
