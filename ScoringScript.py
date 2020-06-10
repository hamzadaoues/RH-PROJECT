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
        score_to_return = score_to_return + config['skills']
    if summary[skill]:
        score_to_return = score_to_return + config['summary']
    if headline[skill]:
        score_to_return = score_to_return + config['headline']
    if experience[skill]:
        score_to_return = score_to_return + config['experience']
    return score_to_return


# class is a set of skills and coefficient
# This function aims to calculate for a profil the corresponding score in a class
# Example of class : front-end , back-end ...
def score_profile_per_class(profile, classe, config):
    final_score = 0
    for skill in classe['skills']:
        final_score = final_score + score_profile_per_skill(profile, skill['skill_name'], config) * skill['skill_coef']
    return format((final_score / classe['score_max']) * 100, '.2f')


DB_PATH = r'files/sample_analyse_new_struct_3.json'
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
    profile_affectation = {"id": profile['id'], 'location': profile['location'],
                           'total_experience': profile['total_experience'], 'stability': profile['stability']}
    max_score = 0
    class_name = False
    for classe in classes:
        score = float(score_profile_per_class(profile, classe, config['scoring']))
        profile_affectation[classe['class_name']] = score
        # Tag the profile with the appropriate class ( which hav the highest score )
        if score > max_score:
            max_score = score
            class_name = classe['class_name']
    profile_affectation['class_name'] = class_name
    profile_affectation['score'] = max_score
    profiles.append(profile_affectation)

json_profiles = json.dumps(profiles)
file = open('files/sample_recommendation_approach2.json', "w")
file.write(json_profiles)
file.close()

# For visualisation
# df = pd.DataFrame(profiles)
# df.to_excel('sample_analyse_result_4.xlsx')
