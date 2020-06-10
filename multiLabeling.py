# This script aims to assign each CV to corresponding classes
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Import the final structure & defined classes
RESULT_PATH = r'data/db_analyse_result.xlsx'
CLASS_PATH = r'data/classes.json'

# Load the classes ( JSON format )
f = open(CLASS_PATH, "r")
classes = json.load(f)
f.close()
# Load Scoring result
df = pd.read_excel(RESULT_PATH)

# Data Visualisation
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print(df.describe())
# Normalize the Dataset
scaler = MinMaxScaler()
profile_list = ['backend','frontend','phpsymfony','ArchitecteJee','Embedded','fullstackjs','java/jee','DRUPAL','PO']
df[profile_list] = scaler.fit_transform(df[profile_list])
print(df.describe())
columns = ['id'] + profile_list
df_bins = df[columns].copy()
for profile in profile_list:
    df_bins[profile] = pd.cut(df_bins[profile], bins=np.linspace(0, 1, 8), include_lowest=True)
    print(df_bins[profile].value_counts().sort_index())

# For visualisation
df = pd.DataFrame(df)
df.to_excel('db_normalized_result.xlsx')


# MultiLabel Classification
final_df = df.copy()
for index, profile in final_df.iterrows():
    for classe in classes:
        if profile[classe['class_name']] >= 0.429:
            final_df.loc[index, classe['class_name']] = 1
        else:
            final_df.loc[index, classe['class_name']] = 0

# Export the final classification
final_df.to_excel('final_result.xlsx')
df.to_json(r'final_result.json', orient='records')



