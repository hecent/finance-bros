from flask import Flask, render_template
import os

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
    "scenario": "Your friends invite you out the night before an assignment is due.",
    "balance": 100,
    "happiness": 70,
    "grades": 80,
    "choices": [
        {"id": 1, "text": "Stay home and finish the assignment"},
        {"id": 2, "text": "Go out with friends"}
    ]
}

@app.route("/state")
def get_state():
    return jsonify(game_state)


from flask import request, jsonify

@app.route("/choose", methods=["POST"])
def choose():
    data = request.json
    choice_id = data["choice_id"]

    print("User chose:", choice_id)

    # update game state here

    if choice_id == 1:
        game_state["grades"] += 5
        game_state["happiness"] -= 5
        game_state["scenario"] = "You finished your assignment and feel relieved."
    elif choice_id == 2:
        game_state["balance"] -= 20
        game_state["happiness"] += 10
        game_state["grades"] -= 5
        game_state["scenario"] = "You had fun but your assignment suffered."

    game_state["week"] += 1

    return jsonify(game_state)




if __name__ == "__main__":
    app.run(debug=True)