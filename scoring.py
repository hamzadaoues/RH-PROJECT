import json
import pandas as pd
import openpyxl

# this function return the score of a skill in a profile ( have to be customized )
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
# This function aims to calculate for a profile the corresponding score in a class
# Example of class : front-end , back-end ...
def score_profile_per_class(profile, classe, config):
    final_score = 0
    for skill in classe['skills']:
        final_score = final_score + score_profile_per_skill(profile, skill['skill_name'], config) * skill['skill_coef']
    return format((final_score / classe['score_max']) * 100, '.2f')


DB_PATH = r'data/db_analyse_new_struct.json'
CLASS_PATH = r'data/classes.json'
CONFIG_PATH = r'data/config.json'
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
    profile_affectation = {"id": profile['id']}
    max_score = 0
    class_name = False
    for classe in classes:
        score = float(score_profile_per_class(profile, classe, config['scoring']))
        profile_affectation[classe['class_name']] = score
        # Tag the profile with the appropriate class ( which hav the highest score ) classification simple
        #if score > max_score:
            #max_score = score
            #class_name = classe['class_name']
    #profile_affectation['class_name'] = class_name
    #profile_affectation['score'] = max_score
    profiles.append(profile_affectation)

json_profiles = json.dumps(profiles)
file = open('data/db_analyse_result.json', "w")
file.write(json_profiles)
file.close()

# For visualisation
df = pd.DataFrame(profiles)
df.to_excel('data/db_analyse_result.xlsx')


