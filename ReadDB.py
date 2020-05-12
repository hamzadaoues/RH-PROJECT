from ExtractSkills import ExtractSkills


class ReadDB:
    def __init__(self, skillExtractor: ExtractSkills):
        self.skillExtractor = skillExtractor

    # this method returns all words in the headline
    def getProfileHeadlineWords(self, profile):
        text = profile['personal_info']['headline']
        return self.skillExtractor.tokenization(text)

    # this method returns all words in the Summary
    def getProfileSummaryWords(self, profile):
        text = profile['personal_info']['summary']
        return self.skillExtractor.tokenization(text)

    # this method returns all words in the experiences
    def getProfileExperienceWords(self, profile):
        text = ''
        for job in profile['experiences']['jobs']:
            if job['description']:
                text = text + job['description']
                text = text + ' '
            if job['title']:
                text = text + job['title']
                text = text + ' '
        return self.skillExtractor.tokenization(text)

    # this method returns all words in the skills
    def getProfileSkillsWord(self, profile):
        text = ''
        for item in profile['skills']:
            if item['name']:
                text = text + item['name']
                text = text + ' '
        return self.skillExtractor.tokenization(text)
