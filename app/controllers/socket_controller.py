from flask_socketio import emit, disconnect
from app import socketio


@socketio.on("ping", namespace="/")
def ping_pong(data):
    """Test Websocket"""
    emit("pong")


@socketio.on("connect", namespace="/")
def connect_client(data):
    """Fonction to handle connection event"""
    print("Client disconnected")


@socketio.on("disconnect", namespace="/")
def disconnect_client(data):
    """Fonction to handle disconnection event"""
    disconnect()
    print("Client disconnected")
