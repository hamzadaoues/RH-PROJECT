import json
import pandas as pd
import openpyxl
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Calculate Score of a skill in a profile ( have to be customized )
def score_profile_per_skill(profile, skill, config):
    score_to_return = 0
    headline = profile['headline']
    experience = profile['experience']
    summary = profile['summary']
    skills = profile['skills']
    if skills[skill]:
        score_to_return = score_to_return + config['skills']
    if summary[skill]:
        score_to_return = score_to_return + config['summary']
    if headline[skill]:
        score_to_return = score_to_return + config['headline']
    if experience[skill]:
        score_to_return = score_to_return + config['experience']
    return score_to_return


# class is a set of skills and coefficient
# Calculate for a profile the corresponding score in a class
# Example of class : front-end , back-end ...
def score_profile_per_class(profile, classe, config):
    final_score = 0
    for skill in classe['skills']:
        final_score = final_score + score_profile_per_skill(profile, skill['skill_name'], config) * skill['skill_coef']
    return format((final_score / classe['score_max']) * 100, '.2f')

# File paths
DB_PATH = r'data/db_analyse_new_struct.json'
CLASS_PATH = r'data/classes.json'
CONFIG_PATH = r'data/config.json'

# Load classes
f = open(CLASS_PATH, "r")
classes = json.load(f)
f.close()

# Load the database with its new structure
f = open(DB_PATH, "r")
profile_list = json.load(f)
f.close()

# Load the configuration
f = open(CONFIG_PATH, "r")
config = json.load(f)
f.close()

# Compute Scores for each CV
for profile in profile_list:
    max_score = 0
    class_name = False
    for classe in classes:
        score = float(score_profile_per_class(profile, classe, config['scoring']))
        column = "score_"+classe['class_name']
        profile[column] = score
# Classify CVs
df = pd.DataFrame(profile_list)
# 1- Normalize the Dataset
scaler = MinMaxScaler()
profiles = ['score_backend', 'score_frontend', 'score_phpsymfony', 'score_ArchitecteJee', 'score_Embedded', 'score_fullstackjs', 'score_java/jee', 'score_DRUPAL', 'score_PO']
df[profiles] = scaler.fit_transform(df[profiles])
# 2- Classification
for index, profile in df.iterrows():
    for classe in classes:
        column = "score_"+classe['class_name']
        if profile[column] >= 0.429:
            df.loc[index, classe['class_name']] = 1
        else:
            df.loc[index, classe['class_name']] = 0


# Export the final classification
df.to_excel('data/labeled_db.xlsx')
df.to_json(r'data/labeled_db.json', orient='records')


