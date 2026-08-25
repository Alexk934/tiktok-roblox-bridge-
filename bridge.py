from flask import Flask, request, jsonify
from collections import deque
import threading

app = Flask(__name__)

events = deque()
lock = threading.Lock()

SECRET = "cheler48_bridge_2026"


@app.route("/gift", methods=["POST"])
def receive_gift():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "invalid json"}), 400

    if data.get("secret") != SECRET:
        return jsonify({"error": "unauthorized"}), 403

    event = {
        "type": "gift",
        "username": data.get("username"),
        "gift": data.get("gift"),
        "coins": int(data.get("coins", 0))
    }

    with lock:
        events.append(event)

    print("ROBLOX EVENT:", event)

    return jsonify({"success": True})


@app.route("/events", methods=["GET"])
def get_events():

    if request.args.get("secret") != SECRET:
        return jsonify({"error": "unauthorized"}), 403

    result = []

    with lock:
        while events:
            result.append(events.popleft())

    return jsonify(result)


@app.route("/", methods=["GET"])
def home():
    return "TikTok Roblox Bridge ONLINE"


if __name__ == "__main__":
    print("================================")
    print("TIKTOK ROBLOX BRIDGE")
    print("================================")
    print("Bridge pornit pe portul 5000")
    print()

    app.run(host="0.0.0.0", port=5000)