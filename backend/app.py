from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Sample chatbot responses
responses = {
    "hello": ["Hi there!", "Hello!", "Hey! How can I help?"],
    "how are you": ["I'm just a bot, but I'm doing fine!", "I'm great! What about you?"],
    "bye": ["Goodbye!", "See you later!", "Bye! Have a great day!"],
}

def chatbot_response(message):
    """Generate a chatbot response based on input message"""
    message = message.lower().strip()
    for key in responses:
        if key in message:
            return random.choice(responses[key])
    return "I'm not sure how to respond to that."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/2")
def index2():
    return render_template("index2.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from frontend"""
    user_message = request.json.get("message", "")
    bot_reply = chatbot_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
