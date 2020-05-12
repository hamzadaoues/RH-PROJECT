import pandas as pd
import json


# this function return the score of a skill in a profile ( hav to eb customized)
def score_profile_per_skill(profile, skill, config):
    score_to_return = 0
    headline = profile['headline']
    experience = profile['experience']
    summary = profile['summary']
    skills = profile['skills']
    if skills[skill]:
        score_to_return = score_to_return + 1
    if summary[skill]:
        score_to_return = score_to_return + 1
    if headline[skill]:
        score_to_return = score_to_return + 2
    if experience[skill]:
        score_to_return = score_to_return + 3
    return score_to_return


# class is a set of skills and coefficient
# This function aims to calculate for a profil the corresponding score in a class
# Example of class : front-end , back-end ...
def score_profile_per_class(profile, classe, config):
    final_score = 0
    for skill in classe['skills']:
        final_score = final_score + score_profile_per_skill(profile, skill['skill_name'], config) * skill['skill_coef']
    return final_score


DB_PATH = r'C:\Users\User\Desktop\PFA\classification\projet\1.json'
CLASS_PATH = r'C:\Users\User\Desktop\PFA\classification\projet\classes.json'
CONFIG_PATH = r'C:\Users\User\Desktop\PFA\classification\projet\config.json'
# Load the classes ( JSON format )
f = open(CLASS_PATH, "r")
classes = json.load(f)
f.close()

# Load the database ( in JSON format )
f = open(DB_PATH, "r")
profile_list = json.load(f)
f.close()

# Load the configuration ( in JSON format )
f = open(CONFIG_PATH, "r")
config = json.load(f)
f.close()

profiles = []
for profile in profile_list:
    profile_affectation = {'id': profile['id']}
    for classe in classes:
        score = score_profile_per_class(profile, classe, config)
        profile_affectation[classe['class_name']] = score
    profiles.append(profile_affectation)
df = pd.DataFrame(profiles)
print(df)
df.to_excel('result.xlsx')
