from flask import render_template, jsonify
from app import app, socketio


# List to store sent messages
sent_messages = []


@app.route("/socket_form")
def socket_form():
    """Route to render the Flask-SocketIO HTML page."""
    return render_template("flask_socketio.html")


@app.route("/socket_messages")
def get_all_messages():
    """Route to get all sent messages in JSON format."""
    return jsonify(sent_messages)


@socketio.on("connect")
def handle_connect():
    socketio.emit("all_messages", sent_messages)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("message")
def handle_message(data):
    sent_messages.append(data)
    socketio.emit("response", data)
    socketio.emit("all_messages", sent_messages)
