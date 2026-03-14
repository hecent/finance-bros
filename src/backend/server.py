from flask import Flask, render_template, request, jsonify
import os
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os
from random import random

load_dotenv()
API_KEY = os.getenv("geminiKEY")

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
    "balance": 1000,
    "happiness": 50,
    "grades": 12,
    "choices": [
        # {"id": 1, "text": "Stay home and finish the assignment"},
        # {"id": 2, "text": "Go out with friends"}
    ]
}





class Effect(BaseModel):
    money: float = Field(description="How the option will affect the balance (+/- number in pounds)")
    happiness: float = Field(description="How the option will affect the happiness (+/- number on a clamped 0-100 point scale)")
    grades: float = Field(description="How the option will affect the grade (+/- number on clamped 20 point scale)")

class Option(BaseModel):
    text: str = Field(description="Text for the option")
    effect: Effect

class Scenario(BaseModel):
    description: str = Field(description="Question to pose the user")
    options: List[Option]

client = genai.Client(api_key=API_KEY)

prompt = """
This is a game where you play as a CS student at st andrews, each week you are given multiple different random decisions to make that can affect balance, happiness and grades. Given a probability you should create a random decison with options and outcomes (grades follow a 20-point scale, happiness is 0-100, balance is in £ and can go negative). The probability affects how liekly the event should be, with a high probability being something simple like going to cafe and a low probability being a major event like a house fire or getting drafted for ww3. The focus of the game is about teaching students money skills but also be fun and humorous at the same times, bear that in mind. A decision can have an umilimited number of options, or even just one option if its something like an event.

E.g:
{
      "description": "You have a major Computer Science project due tomorrow, but your code is throwing endless errors.",
      "options": [
        {
          "text": "Stay up all night debugging.",
          "effect":{
          "money": -5.0,
          "happiness": -10.0,
          "grades": 1.5}
        },
        {
          "text": "Submit what you have and go to sleep.",
          "effect":{
          "money": 0.0,
          "happiness": 8.0,
          "grades": -1.5}
        },
        {
          "text": "Pay a tutor for emergency help.",
          "effect":{
          "money": -40.0,
          "happiness": -2.0,
          "grades": 1.0}
        }
      ]
}
"""

option_effects = []

def getNewLevel():
    global option_effects
    dm = DecisionManager("decisions.json")
    if random()>0.9:
        currentdecision = dm.pick_and_remove()
    else:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": Scenario.model_json_schema(),
            },
            )
        currentdecision = Scenario.model_validate_json(response.text)

        
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
    print(game_state)
    if game_state["scenario"] == "":
        getNewLevel()
    print(game_state)
    return jsonify(game_state)

@app.route("/choose", methods=["POST"])
def choose():
    data = request.get_json()
    print("data", data)
    choice_id = data["choice_id"]

    print("User chose:", choice_id)

    print(choice_id, option_effects)

    effects = option_effects[choice_id]
    game_state["grades"] += effects["gradesCh"]
    game_state["happiness"] += effects["happinessCh"]
    game_state["balance"] += effects["balanceCh"]
    game_state["week"] += 1

    if (game_state["week"] > 12):
        print("AHHASDLF;HJASD;LFGHEWARFDPOAHFGPOSDZIHFGPAWSHDHWEPIOUHFPADHPASDHFSOLKFHAPEHRFPOW")


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