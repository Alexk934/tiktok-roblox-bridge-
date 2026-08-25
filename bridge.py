from flask import Flask, request, jsonify
from collections import deque
import threading

app = Flask(__name__)

events = deque()
lock = threading.Lock()

SECRET = "cheler48_bridge_2026"


# ==========================================
# GIFT
# ==========================================

@app.route("/gift", methods=["POST"])
def receive_gift():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "invalid json"}), 400

    if data.get("secret") != SECRET:
        return jsonify({"error": "unauthorized"}), 403

    try:
        coins = int(data.get("coins", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid coins"}), 400

    event = {
        "type": "gift",
        "username": data.get("username"),
        "gift": data.get("gift"),
        "coins": coins
    }

    with lock:
        events.append(event)

    print("ROBLOX GIFT EVENT:", event)

    return jsonify({"success": True})


# ==========================================
# COMMENT
# ==========================================

@app.route("/comment", methods=["POST"])
def receive_comment():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "invalid json"}), 400

    if data.get("secret") != SECRET:
        return jsonify({"error": "unauthorized"}), 403

    username = str(data.get("username", "")).strip()
    comment = str(data.get("comment", "")).strip()

    if not username:
        return jsonify({"error": "missing username"}), 400

    if not comment:
        return jsonify({"error": "missing comment"}), 400

    event = {
        "type": "comment",
        "username": username,
        "comment": comment
    }

    with lock:
        events.append(event)

    print("ROBLOX COMMENT EVENT:", event)

    return jsonify({"success": True})


# ==========================================
# EVENTS
# ==========================================

@app.route("/events", methods=["GET"])
def get_events():

    if request.args.get("secret") != SECRET:
        return jsonify({"error": "unauthorized"}), 403

    result = []

    with lock:
        while events:
            result.append(events.popleft())

    return jsonify(result)


# ==========================================
# HOME
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return "TikTok Roblox Bridge ONLINE"


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    print("================================")
    print("TIKTOK ROBLOX BRIDGE")
    print("================================")
    print("Bridge pornit pe portul 5000")
    print()

    app.run(
        host="0.0.0.0",
        port=5000
    )