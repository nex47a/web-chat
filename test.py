from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

MESSAGES_FILE = "messages.json"

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_messages(messages):
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


@app.route("/")
def chatroom():
    messages = load_messages()
    return render_template("chat.html", messages=messages)


@socketio.on("send_message")
def handle_message(data):
    user = data.get("user", "Anon")
    msg = data.get("msg", "")
    if msg.strip() == "":
        return


    messages = load_messages()
    messages.append({"user": user, "msg": msg})
    save_messages(messages)

    emit("message", {"user": user, "msg": msg}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)