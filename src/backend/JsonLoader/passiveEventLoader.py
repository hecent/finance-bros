import json
from model.PassiveEvent import PassiveEvent
from model.Effect import Effect

def load_passive_events(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    events = []

    for event in data["passive_events"]:
        effect = Effect (
            money = event["money_change"],
            happiness= event["happiness_change"],
            grades= event ["grades_change"]
        )

        event = PassiveEvent(
            event_id=data["id"]
            
        )
