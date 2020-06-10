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
        character_to_remove = ['/', '/n', '-', ')', '(', '.', ';', ':', '=', '!', '?', '#', '_', '<', '>', "'", ",",
                               "[", "]",
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
            if word.lower() not in ['the', 'a', 'when',
                                    'do', 'with', 'we', 'our', 'it', 'its', 'in', 'on', 'or', 'and', 'them', 'their',
                                    'of', 'at', 'after', 'before', 'to', 'from']:
                lexeme = self.nlp.vocab[word]
                if not lexeme.is_stop:
                    filtered_sentence.append(word.lower())
        return filtered_sentence

    # This method checks if two words matches according to a threshold
    # The parameter subs : if True use parial_ratio for matching
    def two_words_match(self, word1, word2, threshold, subs=False) -> bool:
        if fuzz.ratio(word1.lower(), word2.lower()) > threshold:
            return True
        else:
            if subs:
                return fuzz.partial_ratio(word1.lower(), word2.lower()) > threshold
            else:
                return False

    # This method returns a list of word that matches the word skill with some precision ( we can modify the precision )
    def extractSkillMatchers(self, list_word, skill):
        list_matchers = []
        for word in list_word:
            threshold = 80
            if len(word) < 4 or len(skill) < 4:
                threshold = 85
            if self.two_words_match(word.lower(), skill, threshold):
                list_matchers.append(word.lower())
        return list_matchers

    # this function checks if a word matches an element in the list
    def word_match_list(self, word, skills_list, threshold) -> bool:
        for skill in skills_list:
            checked = False
            if len(word) < 4 or len(skill) < 4:
                checked = word == skill
            else:
                checked = self.two_words_match(word, skill, threshold)
            if checked:
                return True
        return False
