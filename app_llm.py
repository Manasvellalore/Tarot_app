from flask import Flask, render_template, request, jsonify
import random
import os
import requests
from tarot_cards import tarot_deck

# Set your Together API key
TOGETHER_API_KEY = "83ffb2d59bfa48f715138f593cd0d8bee5cbb31a0a2bf90699a391675a191c38"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

app = Flask(__name__)

def get_llm_reading(question, cards):
    card_descriptions = "\n".join([
        f"{card['name']}: {card['deep_meaning']['upright']}" for card in cards
    ])

    prompt = f"""
The user asked: "{question}"

The following tarot cards were drawn:
{', '.join([card['name'] for card in cards])}

Card meanings:
{card_descriptions}

Please provide a deep, intuitive, and context-aware interpretation based on the question and the cards. The tone should be thoughtful, compassionate, and insightful.
"""

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {
                "role": "system",
                "content": "You are a master tarot reader providing insightful, personalized guidance."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8,
        "max_tokens": 800
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=data)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)  # Show raw response for debugging

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Exception occurred: {e}"


@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/get_reading", methods=["POST"])
def get_reading():
    data = request.get_json()
    question = data.get("question", "")
    selected_cards = random.sample(tarot_deck, 3)

    llm_response = get_llm_reading(question, selected_cards)

    return jsonify({
        "cards": selected_cards,
        "llm_reading": llm_response
    })

if __name__ == "__main__":
    app.run(debug=True)