from datetime import datetime
import json
import pandas as pd
import codecs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from fuzzywuzzy import fuzz

import pandas as pd

from ExtractSkills import ExtractSkills
from ReadDB import ReadDB

DB_PATH = r'data/database_brute.json'
Extractor = ExtractSkills()
DB_reader = ReadDB(Extractor)

# List of matchers for each skill
skills_matching_list = {}

# Load the matchers list for each skill
SKILL_MATCHERS_PATH = r'data/skills.json'
f = open(SKILL_MATCHERS_PATH, "r")
skills_matching_list = json.load(f)

# Load the original database ( in JSON format )
data_frame = pd.read_json(DB_PATH, lines=True, encoding='utf-8')

# List that will hold new profiles ( with new structure )
new_profiles = []

# Load Schools dict
df_schools = pd.read_excel(r'data\schools_dict.xlsx')

# Extract Skills list from classes.json
def extract_skill_list():
    df = pd.read_json(r'data\classes.json')
    skill_list = []
    for ind in df.index:
        skills = df['skills'][ind]
        for skill in skills:
            skill_list.append(skill["skill_name"])
    return skill_list

# Assign for each profile a location ( 0 if Tunisia , 1 if French and 2 if others )
def update_location(personal_info):
    for pers in personal_info:
        if pers['location']:
            location = pers['location'].lower()
            if "tunisia" in location or "tunisie" in location:
                location = 0
            elif "france" in location:
                location = 1
            else:
                location = 2
        else:
            location = 2
        pers['location'] = location
    return personal_info


# Calculate number of months from date range in this form : "Nov 2017 – Jul 2018" "Sep 2018 – Present"
def calcul_months_from_date_range(date_range):
    months_map = {'jan': 1, 'janv.': 1, 'feb': 2, 'mars': 3, 'avr.': 4, 'mai': 5, 'juin': 6, 'jun': 6, 'juil.': 7,
                  'jul': 7, 'août': 8, 'aug': 8, 'sep': 9, 'sept': 9, 'sept.': 9, 'oct.': 10, 'oct': 10, 'nov.': 11,
                  'déc.': 12, 'dec.': 12, 'apr': 4, 'nov': 11, 'févr': 2, 'mar': 3, 'may': 5, 'févr.': 2}
    words_list = date_range.split(' ')
    range_tab = [1, False, 1, False]
    i = 0
    for word in words_list:
        if i < 4 or not word == '-':
            if word == 'Aujourd’hui' or word == 'Present':
                range_tab[i] = datetime.today().month
                i = i + 1
                range_tab[i] = datetime.today().year
            else:
                if word.isnumeric():
                    if i % 2 == 0:
                        i = i + 1
                    range_tab[i] = int(word)
                    i = i + 1
                else:
                    if word.lower() in months_map:
                        range_tab[i] = months_map[word.lower()]
                        i = i + 1
    if not range_tab[3]:
        result = 12
    else:
        result = (range_tab[3] - range_tab[1]) * 12 + range_tab[2] - range_tab[0]
    if result < 1:
        result = 6
    return result


# Calculate the total experience ( in month )
def total_experience_profile(jobs):
    total = 0
    for job in jobs:
        if job['date_range']:
            total = total + calcul_months_from_date_range(job['date_range'])
    return total


# Calculate the average experience ( for the stability field )
def avg_experience_profile(jobs):
    total = 0
    coef = 0
    for job in jobs:
        if job['date_range']:
            coef += 1
            total = total + calcul_months_from_date_range(job['date_range'])
    if coef == 0:
        return 0
    return total / coef

# Clean & classify a given school
def school_process(school) :
    english_stopwords = stopwords.words('english')
    french_stopwords = stopwords.words('french')
    extra_words = ["l'", "d'", "l’", "d’", "'", "’", "\(", "\.", "\)", "tunisia", "tunisie"]
    school_class = 2
    if not school is None:

        # 1 Clean Data

        final_school = school.lower().strip()
        text_tokens = word_tokenize(final_school)
        tokens_without_sw = [word for word in text_tokens if not word in english_stopwords]
        tokens_without_sw = [word for word in tokens_without_sw if not word in french_stopwords]
        final_school = " ".join(tokens_without_sw)
        for word in extra_words:
            final_school = re.sub(word, "", final_school)
        final_school = re.sub(r"é", "e", final_school)
        final_school = re.sub(r"è", "e", final_school)
        final_school = re.sub(r"-", ' ', final_school)

        # Classify School

        text_tokens = word_tokenize(final_school)
        for j in df_schools.index:
            school_tokens = word_tokenize(str(df_schools['school'][j]))
            school_tokens_1 = word_tokenize(str(df_schools['match_1'][j]))
            school_tokens_2 = word_tokenize(str(df_schools['match_2'][j]))
            school_tokens_3 = word_tokenize(str(df_schools['match_3'][j]))
            if all(word in text_tokens for word in school_tokens):
                school_class = df_schools['class'][j]
                break
            elif all(word in text_tokens for word in school_tokens_1):
                school_class = df_schools['class'][j]
                break
            elif all(word in text_tokens for word in school_tokens_2):
                school_class = df_schools['class'][j]
                break
            elif all(word in text_tokens for word in school_tokens_3):
                school_class = df_schools['class'][j]
                break
            else:
                maxi = float(0)
                school_match = fuzz.ratio(str(final_school), str(df_schools['school'][j]))
                school1_match = fuzz.ratio(str(final_school), str(df_schools['match_1'][j]))
                school2_match = fuzz.ratio(str(final_school), str(df_schools['match_2'][j]))
                school3_match = fuzz.ratio(str(final_school), str(df_schools['match_3'][j]))
                scores = [school_match, school1_match, school2_match, school3_match]
                score = max(scores)
                if score > maxi and score >= 91:
                    maxi = score
                    school_class = df_schools['class'][j]
                    break
    return school_class

# Update location
data_frame.personal_info = update_location(data_frame.personal_info)

# Extract skill list
skills_list = extract_skill_list()

# Process
for index, profile in data_frame.iterrows():
    new_profile = {'id': profile['_id']['$oid'], 'location': profile['personal_info']['location'], 'school': 2}
    # Calculate Total experience and avg experience
    total_experience = 0
    stability = 0
    if profile['experiences']['jobs']:
        total_experience = total_experience_profile(profile['experiences']['jobs'])
        stability = avg_experience_profile(profile['experiences']['jobs'])
    new_profile['total_experience'] = total_experience
    new_profile['stability'] = stability
    new_profile['school'] = int(school_process(profile['personal_info']['school']))
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

# Write the new database to file
json_profiles = json.dumps(new_profiles)
final = pd.DataFrame(new_profiles)
#final.to_excel(r'data\test.xlsx', index=False)
file = open('data/db_analyse_new_struct.json', "w")
file.write(json_profiles)
file.close()
