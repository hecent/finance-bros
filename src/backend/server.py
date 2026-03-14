from flask import Flask, render_template
import os
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("geminiKEY")


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
    "question": "Your friends invite you out the night before an assignment is due.",
    "balance": 1000,
    "happiness": 50,
    "grades": 12,
    "options": [
        {"id": 1, "text": "Stay home and finish the assignment"},
        {"id": 2, "text": "Go out with friends"}
    ]
}



class Option(BaseModel):
    choice_id: int = Field(description="Unique option ID")
    option_text: str = Field(description="Text for the option")
    balance_change: float = Field(description="How the option will affect the balance (+/- number in pounds)")
    happiness_change: float = Field(description="How the option will affect the happiness (+/- number on a clamped 0-100 point scale)")
    grades_change: float = Field(description="How the option will affect the grade (+/- number on clamped 20 point scale)")

class Scenario(BaseModel):
    question: str = Field(description="Question to pose the user")
    options: List[Option]

client = genai.Client(api_key=API_KEY)

prompt = """
This is a game where you play as a CS student at st andrews, each week you are given multiple different random decisions to make that can affect balance, happiness and grades. Given a probability you should create a random decison with options and outcomes (grades follow a 20-point scale, happiness is 0-100, balance is in £ and can go negative). The probability affects how liekly the event should be, with a high probability being something simple like going to cafe and a low probability being a major event like a house fire or getting drafted for ww3. The focus of the game is about teaching students money skills but also be fun and humorous at the same times, bear that in mind. A decision can have an umilimited number of options, or even just one option if its something like an event.

E.g:
{
      "question": "You have a major Computer Science project due tomorrow, but your code is throwing endless errors.",
      "options": [
        {
          "choice_id": 1,
          "option_text": "Stay up all night debugging.",
          "balance_change": -5.0,
          "happiness_change": -10.0,
          "grades_change": 1.5
        },
        {
          "choice_id": 2,
          "option_text": "Submit what you have and go to sleep.",
          "balance_change": 0.0,
          "happiness_change": 8.0,
          "grades_change": -1.5
        },
        {
          "choice_id": 3,
          "option_text": "Pay a tutor for emergency help.",
          "balance_change": -40.0,
          "happiness_change": -2.0,
          "grades_change": 1.0
        }
      ]
}
"""

@app.route("/state")
def get_state():
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Scenario.model_json_schema(),
    },
    )
    scenario = Scenario.model_validate_json(response.text)
    game_state["question"] = scenario.question
    game_state["options"] = [option.model_dump() for option in scenario.options]
    print(scenario)
    return jsonify(game_state)


from flask import request, jsonify

@app.route("/choose", methods=["POST"])
def choose():
    data = request.json
    choice_id = data["choice_id"]

    print("User chose:", choice_id)

    # update game state here
    choice = next(option for option in game_state["options"] if option["choice_id"] == choice_id)

    if choice is None:
        return jsonify({"error": "Invalid choice_id"}), 404

    game_state["grades"] += choice["grades_change"]
    game_state["balance"] += choice["balance_change"]
    game_state["happiness"] += choice["happiness_change"]

    game_state["week"] += 1

    response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Scenario.model_json_schema(),
    },
    )
    scenario = Scenario.model_validate_json(response.text)
    game_state["question"] = scenario.question
    game_state["options"] = [option.model_dump() for option in scenario.options]
    print(scenario)
    return jsonify(game_state)




if __name__ == "__main__":
    app.run(debug=True)