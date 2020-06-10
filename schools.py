import pandas as pd
import codecs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Import school classes
df_schools = pd.read_excel(r'data\schools_dict.xlsx')

# Import original Database
df_db = pd.read_json(codecs.open('data\database_brute.json', 'r', 'utf-8'), lines=True)
persons = df_db['personal_info']
_id = df_db['_id']
db_id = []
for id in _id:
    db_id.append(id['$oid'])
db_school = []
for pers in persons:
    db_school.append(pers['school'])
df = pd.DataFrame(
    {'id': db_id,
     'original data school': db_school,
     'class' : ''
     })

# 3- Clean Data
standardized_schools = []
english_stopWords = stopwords.words('english')
french_stopWords = stopwords.words('french')
extra_words = ["l'", "d'", "l’", "d’", "'", "’", "\(", "\.", "\)", "tunisia", "tunisie"]
for ind in df.index:
    if not df['original data school'][ind] is None:
        standardized_schools.append(df['original data school'][ind].lower().strip())
        text_tokens = word_tokenize(standardized_schools[ind])
        tokens_without_sw = [word for word in text_tokens if not word in english_stopWords]
        tokens_without_sw = [word for word in tokens_without_sw if not word in french_stopWords]
        standardized_schools[ind] = " ".join(tokens_without_sw)
        for word in extra_words:
            standardized_schools[ind] = re.sub(word, "", standardized_schools[ind])
        standardized_schools[ind] = re.sub(r"é", "e", standardized_schools[ind])
        standardized_schools[ind] = re.sub(r"è", "e", standardized_schools[ind])
        standardized_schools[ind] = re.sub(r"-", ' ', standardized_schools[ind])

    else:
        standardized_schools.append(None)
# Set school name after process
df['standardized data school'] = standardized_schools

# 4- Data Matching
school_list = df_schools['school'].tolist()
for i in df.index:
    df['class'][i] = 2
    if not df['standardized data school'][i] is None:
        text_tokens = word_tokenize(df['standardized data school'][i])
        for j in df_schools.index:
            school_tokens = word_tokenize(str(df_schools['school'][j]))
            school_tokens_1 = word_tokenize(str(df_schools['match_1'][j]))
            school_tokens_2 = word_tokenize(str(df_schools['match_2'][j]))
            school_tokens_3 = word_tokenize(str(df_schools['match_3'][j]))
            if all(word in text_tokens for word in school_tokens):
                df['standardized data school'][i] = df_schools['school'][j]
                df['class'][i] = df_schools['class'][j]
                break
            elif all(word in text_tokens for word in school_tokens_1):
                df['standardized data school'][i] = df_schools['school'][j]
                df['class'][i] = df_schools['class'][j]
                break
            elif all(word in text_tokens for word in school_tokens_2):
                df['standardized data school'][i] = df_schools['school'][j]
                df['class'][i] = df_schools['class'][j]
                break
            elif all(word in text_tokens for word in school_tokens_3):
                df['standardized data school'][i] = df_schools['school'][j]
                df['class'][i] = df_schools['class'][j]
                break
            else:
                maxi = float(0)
                school_match = fuzz.ratio(str(df['standardized data school'][i]), str(df_schools['school'][j]))
                school1_match = fuzz.ratio(str(df['standardized data school'][i]), str(df_schools['match_1'][j]))
                school2_match = fuzz.ratio(str(df['standardized data school'][i]), str(df_schools['match_2'][j]))
                school3_match = fuzz.ratio(str(df['standardized data school'][i]), str(df_schools['match_3'][j]))
                scores = [school_match, school1_match, school2_match, school3_match]
                score = max(scores)
                if score > maxi and score >= 91:
                    maxi = score
                    df['standardized data school'][i] = df_schools['school'][j]
                    df['class'][i] = df_schools['class'][j]
                    break
df.to_excel(r'data\cleaned_schools.xlsx', index=False)

