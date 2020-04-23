from fuzzywuzzy import fuzz
from spacy.lang.fr import French
import re


class ExtractSkills:
    def __init__(self):
        self.nlp = French()

    # This method converts a text to a list of word + removing the stopwords
    def tokenization(self, text, filtered_sentence=None):
        if not text:
            return []
        character_to_remove = ['/', '-', ')', '(', '.', ';', ':', '=', '!', '?', '#', '_', '<', '>', "'", ",", "[", "]",
                               "{", "}", "&", "|"]
        for c in character_to_remove:
            text = re.sub(re.escape(c), ' ', text)
        self.nlp.max_length = 12532836
        my_doc = self.nlp(text)
        token_list = []
        for token in my_doc:
            token_list.append(token.text)
        filtered_sentence = []
        for word in token_list:
            # We can always update this stopwords
            if word.lower() not in ['/n', '/n/n', '/n/n/n', '/n/n/n/n', 'the', 'a', 'when',
                                    'do', 'with', 'we', 'our', 'it', 'its', 'in', 'on', 'or', 'and', 'them', 'their',
                                    'of', 'at', 'after', 'before', 'to', 'from']:
                lexeme = self.nlp.vocab[word]
                if not lexeme.is_stop:
                    filtered_sentence.append(word)
        return filtered_sentence

    # This method returns a list of word that matches the word skill with some precision ( we can modify the precision )
    def extractSkillMatchers(self, list_word, skill):
        list_matchers = []
        for word in list_word:
            if word.lower() not in list_matchers:
                if fuzz.ratio(word.lower(), skill) > 80:
                    list_matchers.append(word.lower())
                else:
                    if fuzz.partial_ratio(word.lower(), skill) > 80:
                        list_matchers.append(word.lower())
        return list_matchers
