import json
import os
from model.PassiveEvent import PassiveEvent
from model.Effect import Effect

def load_passive_events(filename):
    # Get the absolute path to the directory containing this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to the backend directory where passive_events.json is located
    parent_dir = os.path.dirname(base_dir)
    filepath = os.path.join(parent_dir, filename)
    
    with open(filepath, "r") as f:
        data = json.load(f)

    events = []

    for event_data in data["passive_events"]:
        new_effect = Effect(
            money=event_data.get("money_change", 0.0),
            happiness=event_data.get("happiness_change", 0.0),
            grades=event_data.get("grades_change", 0.0)
        )

        prob = event_data.get("probability", 1.0)
        event_id = event_data.get("id", 0)
        
        event = PassiveEvent(event_id, event_data["message"], new_effect, prob)
        events.append(event)

    return events