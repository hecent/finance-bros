import json
from model.PassiveEvent import PassiveEvent
from model.Effect import Effect

def load_passive_events(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    events = []

    for event in data["passive_events"]:
        new_effect = Effect (
            money=data["money_change"],
            happiness=data["happiness_change"],
            grades=data["grades_change"]
        )

        event = PassiveEvent(data["id"], data["message"], new_effect)
        events.append(event)

    return events