from flask import Flask, request, jsonify, render_template
import requests
import datetime

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

# System prompt (makes chatbot smarter)
SYSTEM_PROMPT = """
You are StudyMate AI, a helpful assistant for students.
Give clear, short, and easy-to-understand answers.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "⚠️ Please enter a message."})

        # Add system instruction
        full_prompt = SYSTEM_PROMPT + "\nUser: " + user_message

        payload = {
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_API_URL, json=payload)
        result = response.json()

        bot_reply = result.get("response", "No response from AI.")

        # Log conversation (for debugging)
        print(f"[{datetime.datetime.now()}]")
        print("User:", user_message)
        print("Bot:", bot_reply)
        print("-" * 40)

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "⚠️ Server error. Try again later."})

if __name__ == "__main__":
    app.run(debug=True)