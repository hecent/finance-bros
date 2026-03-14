import json
import random
from model.Decision import Decision
from model.Option import Option
from model.Effect import Effect

class DecisionManager:
    def __init__(self, filename):
        self.decisions = self.load_decisions(filename)

    def load_decisions(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        weekly_decisions = []

        for tempData in data["weekly_decisions"]:
            options = []
            for tempOption in tempData["options"]:
                effect = Effect(
                    money=tempOption["balance_change"],
                    happiness=tempOption["happiness_change"],
                    grades=tempOption["grades_change"]
                )
                option = Option(tempOption["option_text"], effect)
                options.append(option)

            # Map "probability" from JSON to your weight attribute
            weight = tempData.get("probability", 1.0)
            decision = Decision(tempData["question"], options, weight)
            weekly_decisions.append(decision)

        return weekly_decisions

    def pick_and_remove(self):
        if not self.decisions:
            return None

        # Extract weights for random.choices
        weights = [d.weight for d in self.decisions]
        
        # Select one decision based on weights
        # random.choices returns a list, so we take the first element [0]
        selected_decision = random.choices(self.decisions, weights=weights, k=1)[0]

        # Remove it from the list so it can't be picked again
        self.decisions.remove(selected_decision)

        return selected_decision
