from quote import Quote

class QuoteCollection:
    def __init__(self, object_from_yaml):
        self.deserialise(object_from_yaml)
    
    def deserialise(self, object_from_yaml):
        self.name = object_from_yaml["name"]
        self.tags = object_from_yaml["tags"]
        self.quotes = [Quote(quote_data) for quote_data in object_from_yaml["quotes"]]
    
    def serialise(self):
        return {
            "name": self.name,
            "tags": self.tags,
            "quotes": [quote.serialise() for quote in self.quotes]
        }