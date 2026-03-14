from model.Effect import Effect

class PassiveEvent:
    def __init__(self, event_id, message, effect, probability=1.0):
        self.id = event_id
        self.message = message
        self.effect = effect
        self.probability = probability