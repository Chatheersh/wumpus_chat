class PitModel():
    def __init__(self, model, indexes):
        self.model = model
        self.indexes = indexes

    def predict_proba(self, values):
        return self.model.predict_proba(values)
    
    def fetch_response(self, index, response):
        return response[self.indexes[index]]