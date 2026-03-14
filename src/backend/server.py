from flask import Flask, render_template
import os
from JsonLoader.decisionLoader import DecisionManager

# Get absolute path to frontend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR
)

@app.route("/")
def home():
    return render_template("index.html")


# Simple in-memory game state
game_state = {
    "year": 1,
    "week": 1,
    "scenario": "",
    "balance": 100,
    "happiness": 70,
    "grades": 80,
    "choices": [
        # {"id": 1, "text": "Stay home and finish the assignment"},
        # {"id": 2, "text": "Go out with friends"}
    ]
}

option_effects = []

def getNewLevel():
    global option_effects
    dm = DecisionManager("decisions.json")
    currentdecision = dm.pick_and_remove()
    game_state["scenario"] = currentdecision.description
    newChoices = []
    newOptionEffects = []
    options = currentdecision.options
    count = 1
    for option in options:
        newChoices.append({
            "id": count,
            "text": option.text
            })
        newOptionEffects.append({
            "id": count,
            "balanceCh": option.effect.money,
            "gradesCh": option.effect.grades,
            "happinessCh": option.effect.happiness
        })
        count += 1


    game_state["choices"] = newChoices
    option_effects = newOptionEffects


@app.route("/state")
def get_state():
    if game_state["scenario"] == "":
        getNewLevel()
    return jsonify(game_state)


from flask import request, jsonify

@app.route("/choose", methods=["POST"])
def choose():
    data = request.json
    choice_id = data["choice_id"]

    print("User chose:", choice_id)

    print(choice_id, option_effects)

    effects = next((item for item in option_effects if item["id"] == choice_id), None)#option_effects[choice_id]
    game_state["grades"] += effects["gradesCh"]
    game_state["happiness"] += effects["happinessCh"]
    game_state["balance"] += effects["balanceCh"]
    game_state["week"] += 1

    # update game state here
    # dm = DecisionManager("decisions.json")
    # currentdecision = dm.pick_and_remove()
    # print(currentdecision.description)
    # options = currentdecision.options # Option {str text, Effect effect}
    # for option in options:
    #     print(option.text)

    # if choice_id == 1:
    #     game_state["grades"] += 5
    #     game_state["happiness"] -= 5
    #     game_state["scenario"] = "You finished your assignment and feel relieved."
    # elif choice_id == 2:
    #     game_state["balance"] -= 20
    #     game_state["happiness"] += 10
    #     game_state["grades"] -= 5
    #     game_state["scenario"] = "You had fun but your assignment suffered."


    # after changing the stats
    # game_state["scenario"] = currentdecision.description
    # newChoices = []
    # options = currentdecision.options
    # count = 1
    # for option in options:
    #     newChoices.append({
    #         "id": count,
    #         "text": option.text
    #         })
    #     count += 1

    # game_state["choices"] = newChoices

    # print(game_state)
    getNewLevel()
    toreturn = jsonify(game_state)
    return toreturn




if __name__ == "__main__":
    app.run(debug=True)