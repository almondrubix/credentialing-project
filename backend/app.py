import json
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


# mock function to generate a baseline for a given question
def get_baseline_answer(question):
    baselines = {
        "your team is behind schedule. what do you do?": (
            "I would talk to the team, identify blockers, and set realistic deadlines."
        ),
        "How would you handle resistance from a team member who disagrees with your approach?": (
            "I would listen to their concerns, clarify misunderstandings, and collaborate to find a middle ground."
        ),
    }
    return baselines.get(question, "This is a generic response to the question.")


# mock scoring function
def score_candidate_answer(candidate_answer, baseline):
    # Originality based on how many unique words differ from the baseline
    baseline_words = set(baseline.lower().split())
    candidate_words = set(candidate_answer.lower().split())

    uniqueness = len(candidate_words - baseline_words)

    scores = {
        "uniqueness": uniqueness,
        "teamwork": 4 if "team" in candidate_answer else 2,
        "biz_savvy": 3 if "deadline" in candidate_answer else 1,
        "conscientiousness": 5 if "listen" in candidate_answer else 3,
    }
    return scores


# mock follow-up question
def get_followup_question(candidate_answer):
    return "How would you handle resistance from a team member who disagrees with your approach?"


@app.route("/get_scenario", methods=["GET"])
def get_scenario():
    with open("prompts/scenarios.json") as f:
        scenarios = json.load(f)
    scenario = scenarios[0]["scenario"]

    # silently generate baseline (not sent to the client)
    baseline = get_baseline_answer(scenario)

    # store the baseline in memory or a session (if needed for later scoring)
    os.environ["baseline"] = baseline  # simple for now

    return jsonify({"scenario": scenario})


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    candidate_answer = data.get("answer", "")
    scenario = "your team is behind schedule. what do you do?"  # static for now

    # retrieve the stored baseline
    baseline = os.environ.get("baseline", "Default baseline")

    # calculate scores based on the candidate's answer and the baseline
    scores = score_candidate_answer(candidate_answer, baseline)

    # generate follow-up question and new baseline
    followup_question = get_followup_question(candidate_answer)
    new_baseline = get_baseline_answer(followup_question)
    os.environ["baseline"] = new_baseline

    # store in the database
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO responses (scenario, candidate_answer, baseline, uniqueness, teamwork, biz_savvy, conscientiousness) VALUES (?,?,?,?,?,?,?)",
        (
            scenario,
            candidate_answer,
            baseline,
            scores["uniqueness"],
            scores["teamwork"],
            scores["biz_savvy"],
            scores["conscientiousness"],
        ),
    )
    conn.commit()
    conn.close()

    return jsonify({"scores": scores, "followup_question": followup_question})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
