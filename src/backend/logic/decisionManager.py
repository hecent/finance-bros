import random

class DecisionManager:

    def __init__(self,decisions):
        self.decisions = decisions
        
    def getQuestion(self):

        if not self.decisions:
            return None
        weights = []

        for decision in self.decisions:
            weightValue = decision.weight
            
            weights.append(weightValue)

        chosen_list = random.choices(
            self.decisions,
            weights=weights,  
            k=1     
        )


        chosen_decision = chosen_list[0]

        return chosen_decision