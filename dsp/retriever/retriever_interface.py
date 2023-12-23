class RetrieverInterface:
    def __init__(self, database):
        self.database = database

    def retrieve(self, query):
        return [signature for signature in self.database if query in signature.instructions]
