from flask import Flask, render_template, request
import joblib
import re
import warnings

warnings.filterwarnings("ignore")

# TrustLens Backend
# Model trained using Google Colab
# Designed for Google Cloud deployment
# Follows Google Responsible AI principles

app = Flask(__name__)
model = joblib.load("model/scam_model.pkl")

# Explainable risk weights (Responsible AI)
RISK_WEIGHTS = {
    "urgent": 22,
    "salary": 30,
    "personal_email": 20,
    "no_address": 10,
    "short_text": 8
}

def extract_features(text):
    t = text.lower()
    return {
        "urgent": int(any(w in t for w in ["urgent", "immediately", "hurry", "limited"])),
        "salary": int(bool(re.search(r"₹|\$|salary|per month", t))),
        "personal_email": int(bool(re.search(r"@gmail.com|@yahoo.com|@hotmail.com", t))),
        "no_address": int(not any(w in t for w in ["street", "road", "office", "building"])),
        "short_text": int(len(text.split()) < 80)
    }

def calculate_risk(text, features):
    # Get base probability from ML model safely
    try:
        base = model.predict_proba([text])[0][1] * 100
    except:
        base = 0  # fallback if model fails

    # Sum of feature weights
    extra = sum(RISK_WEIGHTS[k] for k, v in features.items() if v == 1)

    # Normalize extra relative to max possible extra
    max_extra = sum(RISK_WEIGHTS.values())
    normalized_extra = (extra / max_extra) * 100

    # Combine base + normalized extra, capped at 100
    risk_score = min(100, int((base + normalized_extra) / 2))  # average for nuance
    return risk_score

def what_if_simulation(text, features):
    sims = {}
    for k in features:
        new_features = features.copy()
        new_features[k] = 0
        sims[k] = calculate_risk(text, new_features)
    return sims

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("job", "")
    if not text.strip():
        return render_template("result.html", risk=0, label="No Input", color="gray",
                               explanations=[], simulations={}, text=text)

    features = extract_features(text)
    risk = calculate_risk(text, features)
    simulations = what_if_simulation(text, features)

    # Risk label & color
    if risk >= 70:
        label, color = "High Risk", "red"
    elif risk >= 40:
        label, color = "Medium Risk", "orange"
    else:
        label, color = "Low Risk", "green"

    # Feature explanations
    explanations = [(k.replace("_", " ").title(), RISK_WEIGHTS[k]) for k, v in features.items() if v == 1]

    return render_template(
        "result.html",
        risk=risk,
        label=label,
        color=color,
        explanations=explanations,
        simulations=simulations,
        text=text
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)



