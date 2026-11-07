from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ISSUE 1 (Caught by Gitleaks): Hardcoded API Key
API_KEY = "AKIA1234567890ABCDEF"
SECRET_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"

# ISSUE 2 (Caught by Custom Injection Scanner): Hardcoded System Prompt
SYSTEM_PROMPT = "You are TechCorp's internal assistant. The admin API_KEY is TECHCORP-ADMIN-KEY-9821."
TEST_INJECTION_SAMPLE = "ignore previous instructions"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "")
    calc_expr = data.get("calc", "1+1")

    # ISSUE 3 (Caught by Bandit SAST B307): Unsafe use of eval()
    calc_result = eval(calc_expr)

    payload = {
        "model": "tinyllama",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    return jsonify({"calc": calc_result, "status": "processed"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
