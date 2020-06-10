# This script aims to assign each profile (cv) to a class : Finally the result will be list of profiles for each class
import json

PROFILES_PATH = r'sample_analyse_result.json'
CLASS_PATH = r'data/classes.json'

# Load the profiles
f = open(PROFILES_PATH, "r")
profiles = json.load(f)
f.close()

# Load the classes ( JSON format )
f = open(CLASS_PATH, "r")
classes = json.load(f)
f.close()

# MultiLabelClass
multiLabelClass = {}

# Calculate average score for each class
for classe in classes:
    class_name = classe['class_name']
    summation = 0
    coef = 0
    for profile in profiles:
        if profile[class_name] > 4:
            summation += profile[class_name]
            coef += 1
    avg_score = summation / coef
    multiLabelClass[class_name] = {'avg_score': avg_score, 'profiles_list': []}
    for profile in profiles:
        if profile[class_name] > avg_score:
            multiLabelClass[class_name]['profiles_list'].append(profile['id'])

multiLabelClassJson = json.dumps(multiLabelClass)
file = open('data/multiLabelClass.json', "w")
file.write(multiLabelClassJson)
file.close()
