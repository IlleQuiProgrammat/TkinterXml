from quote_lib.quote import Quote

class QuoteCollection:
    def __init__(self, object_from_yaml):
        self.deserialise(object_from_yaml)
    
    def deserialise(self, object_from_yaml):
        self.name = object_from_yaml["name"]
        self.quotes = [Quote(quote_data) for quote_data in object_from_yaml["quotes"]]
    
    @property
    def tags(self):  # TODO: Cache the results of this and update on change
        tags = set()
        for quote in self.quotes:
            for tag in quote.tags:
                tags.add(tag)
        return list(tags)

    def serialise(self):
        return {
            "name": self.name,
            "quotes": [quote.serialise() for quote in self.quotes]
        }