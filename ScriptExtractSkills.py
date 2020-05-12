import pandas as pd
from ExtractSkills import ExtractSkills
from ReadDB import ReadDB
import itertools

DB_PATH = r'C:\Users\User\Desktop\PFA\database_brute.json'
skills_list = ['git', 'scrum', 'testing', 'confluence', 'drupal', 'springboot']
# This map will hold the list of matchers for each skill
skills_matching_list = {}
# Initialize list of matchers for each skill in the skills_list
for skill in skills_list:
    skills_matching_list[skill] = []

Extractor = ExtractSkills()
DB_reader = ReadDB(Extractor)

# Load the database ( in JSON format )
data_frame = pd.read_json(DB_PATH, lines=True, encoding='utf-8')

# Extracting matching skills
for index, profile in data_frame.iterrows():
    word_list = list(
        itertools.chain.from_iterable(
            [DB_reader.getProfileSkillsWord(profile), DB_reader.getProfileExperienceWords(profile),
             DB_reader.getProfileSummaryWords(profile), DB_reader.getProfileHeadlineWords(profile)]))
    for skill in skills_list:
        word_extracted = Extractor.extractSkillMatchers(word_list, skill)
        for word in word_extracted:
            if word not in skills_matching_list[skill]:
                skills_matching_list[skill].append(word)

# Writing matching words to xlsx files
for skill in skills_list:
    data_frame = pd.DataFrame(skills_matching_list[skill])
    data_frame.to_excel(skill + '.xlsx')
