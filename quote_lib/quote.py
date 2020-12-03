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