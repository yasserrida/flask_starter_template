"""" Socket IO Controller """

from flask import render_template, jsonify
from flask_socketio import emit, disconnect
from app import app, socketio


# List to store sent messages
sent_messages = []


@app.route("/api/flask_socketio")
def socket():
    """Route to render the Flask-SocketIO HTML page."""

    return render_template("flask_socketio.html")


@app.route("/api/messages")
def get_sent_messages():
    """Route to get all sent messages in JSON format."""

    return jsonify(sent_messages)


@socketio.on("connect")
def handle_connect():
    """Route to connect client."""

    print("Client connected")
    emit("all_messages", sent_messages)


@socketio.on("disconnect")
def handle_disconnect():
    """Route to disconnect client."""

    print("Client disconnected")
    disconnect()


@socketio.on("message")
def handle_message(data):
    """Route to emit data."""

    print("Received message:", data)
    sent_messages.append(data)
    emit("response", data)
    emit("all_messages", sent_messages)
