import json
import RecommendationEngine
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DB_PATH = r'C:\Users\User\Desktop\PFA\classification\projet\files\sample_recommendation_approach2.json'

df = pd.read_json(DB_PATH)
scaler = MinMaxScaler()
column_list = ['total_experience', 'stability', 'location', 'backend', 'frontend', 'phpsymfony', 'ArchitecteJee',
               'Embedded', 'fullstackjs', 'java/jee', 'DRUPAL', 'PO']
df[column_list] = scaler.fit_transform(df[column_list])

profile_list = json.loads(df.to_json(orient='records'))

profile_vector_list = []
for profile in profile_list:
    if profile['id'] == '5e20582f2d080b22a8f77e89':
        profile_to_test = RecommendationEngine.RecommendationEngine.profile_to_vector(profile)
        print(profile_to_test)
    else:
        profile_vector_list.append(RecommendationEngine.RecommendationEngine.profile_to_vector(profile))
lise_recommended = RecommendationEngine.RecommendationEngine.get_similar_profiles(profile_to_test, profile_vector_list,
                                                                                  7)
print(lise_recommended)
