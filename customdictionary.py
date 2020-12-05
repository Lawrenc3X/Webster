from spellchecker import SpellChecker

spell = SpellChecker()

class ServerDictionnary(SpellChecker):
    """server-wide dictionary"""

class UserDictionary(SpellChecker):
    """user-specific dictionary that checks with multiple ServerDictionaries and SpellChecker"""
    def add(self, word):
        """add a word to the custom dictionary"""
        self.word_frequency.dictionary[word] = 1
