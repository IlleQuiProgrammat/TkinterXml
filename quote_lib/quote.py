import difflib
from typing import List

class Quote:
    def __init__(self, object_from_yaml):
        self.deserialise(object_from_yaml)
    
    def deserialise(self, object_from_yaml):
        self.phrase = object_from_yaml["phrase"]
        self.tags = object_from_yaml["tags"]
        self.available = object_from_yaml["available"]
        self.correct = object_from_yaml["correct"]

    def serialise(self):
        return {
            "phrase": self.phrase,
            "tags": self.tags,
            "available": self.available,
            "correct": self.correct,
        }

def get_quote(phrase, quotes):
        for quote in quotes:
            if phrase == quote.phrase:
                return quote
        return None

def get_quote_fuzzy(phrase, quotes, closeness):
    lookup = {quote.phrase: quote for quote in quotes}
    results = difflib.get_close_matches(phrase, [quote.phrase for quote in quotes], 1, closeness)
    # If there is more than one quote which is similar then precision matters
    if len(results) == 1:
        return lookup[results[0]]
    return None
