"""
UPSC Prep Tool — backend server (Flask)

This file wires the website to the AI agents. The actual AI work lives in the
"agents/" folder — this file just handles web requests and calls the agents.

Run it with:  python app.py
Then open:     http://127.0.0.1:5000
"""

import json

from flask import Flask, render_template, jsonify, request

from agents import evaluator
from agents.orchestrator import handle as orchestrate

app = Flask(__name__)

# Load subject notes once, when the server starts.
with open("data/subjects.json", "r", encoding="utf-8") as f:
    SUBJECTS = json.load(f)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.route("/api/subjects")
def get_subjects():
    """Notes + practice questions for the Learn tab."""
    return jsonify(SUBJECTS)


@app.route("/api/evaluate", methods=["POST"])
def evaluate_answer():
    """Structured evaluation (the Evaluate tab): question + answer + word limit."""
    data = request.get_json()
    question = (data.get("question") or "").strip()
    answer = (data.get("answer") or "").strip()
    word_limit = data.get("wordLimit", 250)

    if not question or not answer:
        return jsonify({"error": "Please provide both a question and an answer."}), 400

    try:
        return jsonify(evaluator.evaluate(question, answer, word_limit))
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {e}"}), 500


@app.route("/api/ask", methods=["POST"])
def ask():
    """
    The multi-agent endpoint. The aspirant types anything; the orchestrator
    routes it to the right specialist agent and returns the answer.
    """
    data = request.get_json()
    user_input = (data.get("input") or "").strip()

    if not user_input:
        return jsonify({"error": "Type something first."}), 400

    try:
        return jsonify(orchestrate(user_input))
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {e}"}), 500


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
