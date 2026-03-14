import json

from model.Decision import Decision
from model.Option import Option
from model.Effect import Effect

def load_decisions(filename):
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

        decision = Decision(tempData["question"], options)
        weekly_decisions.append(decision)

    return weekly_decisions