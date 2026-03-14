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

    return jsonify(game_state)




if __name__ == "__main__":
    app.run(debug=True)