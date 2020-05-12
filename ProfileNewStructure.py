import json

import pandas as pd

from ExtractSkills import ExtractSkills
from ReadDB import ReadDB

DB_PATH = r'C:\Users\User\Desktop\PFA\classification\sample1.json'
Extractor = ExtractSkills()
DB_reader = ReadDB(Extractor)

skills_list = ['java', 'expressjs', 'sql', 'nosql', 'javascript', 'koajs', 'hapijs', 'nodejs', 'angularjs', 'reactjs',
               'jquery', 'bash', 'nginx', 'c', 'c++', 'symfony', 'restful', 'git', 'php']
# This map will hold the list of matchers for each skill
skills_matching_list = {}

# Load the matchers list for each skill
SKILL_MATCHERS_PATH = r'C:\Users\User\Desktop\PFA\dictionnary\skills.json'
f = open(SKILL_MATCHERS_PATH, "r")
skills_matching_list = json.load(f)

# Load the database ( in JSON format )
data_frame = pd.read_json(DB_PATH, lines=True, encoding='utf-8')
# list that will hold new profiles ( with new structure )
new_profiles = []

for index, profile in data_frame.iterrows():
    new_profile = {'id': profile['_id']['$oid']}
    # Extract words from the different areas of the profile
    headline_words = DB_reader.getProfileHeadlineWords(profile)
    summary_words = DB_reader.getProfileSummaryWords(profile)
    skills_words = DB_reader.getProfileSkillsWord(profile)
    experience_words = DB_reader.getProfileExperienceWords(profile)
    # Initialization
    new_profile['headline'] = {}
    new_profile['summary'] = {}
    new_profile['experience'] = {}
    new_profile['skills'] = {}
    # Find out skills in each area
    for skill in skills_list:
        new_profile['headline'][skill] = 0
        new_profile['summary'][skill] = 0
        new_profile['skills'][skill] = 0
        new_profile['experience'][skill] = 0
        for words in skills_matching_list[skill]:
            # Find out skills in headline area
            if not new_profile['headline'][skill] and Extractor.word_match_list(words, headline_words, 97):
                new_profile['headline'][skill] = 1
            # Find out skills in summary area
            if not new_profile['summary'][skill] and Extractor.word_match_list(words, summary_words, 97):
                new_profile['summary'][skill] = 1
            # Find out skills in skills area
            if not new_profile['skills'][skill] and Extractor.word_match_list(words, skills_words, 97):
                new_profile['skills'][skill] = 1
            # Find out skills in experience area
            if not new_profile['experience'][skill] and Extractor.word_match_list(words, experience_words, 97):
                new_profile['experience'][skill] = 1

    new_profiles.append(new_profile)
# write the new database to file
json_profiles = json.dumps(new_profiles)
file = open('1.json', "w")
file.write(json_profiles)
file.close()
