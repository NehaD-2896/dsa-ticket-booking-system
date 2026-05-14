import re
from flask import Flask, request, jsonify, send_file
from service import BookingService

app     = Flask(__name__)
service = BookingService()


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/movies")
def movies():
    return jsonify(service.get_movies())


@app.route("/api/shows/<movie_id>")
def shows(movie_id):
    return jsonify(service.get_shows_for_movie(movie_id))


@app.route("/api/seatmap/<show_id>")
def seat_map(show_id):
    data = service.get_seat_map(show_id)
    if not data:
        return jsonify({"error": "Show not found"}), 404
    return jsonify(data)


@app.route("/api/lock", methods=["POST"])
def lock():
    body      = request.get_json()
    show_id   = body.get("show_id")
    seat_ids  = body.get("seat_ids", [])
    user_name = body.get("user_name", "").strip()
    if not show_id or not seat_ids:
        return jsonify({"success": False, "message": "show_id and seat_ids required"}), 400
    return jsonify(service.lock_seats(show_id, seat_ids, user_name))


@app.route("/api/confirm", methods=["POST"])
def confirm():
    body       = request.get_json()
    show_id    = body.get("show_id")
    session_id = body.get("session_id")
    user_name  = body.get("user_name", "").strip()
    seat_ids   = body.get("seat_ids", [])
    if not all([show_id, session_id, user_name, seat_ids]):
        return jsonify({"success": False, "message": "Missing fields"}), 400
    return jsonify(service.confirm_booking(show_id, session_id, user_name, seat_ids))


@app.route("/api/cancel/<booking_id>", methods=["POST"])
def cancel(booking_id):
    return jsonify(service.cancel_booking(booking_id))


@app.route("/api/bookings")
def bookings():
    return jsonify(service.get_all_bookings())


@app.route("/api/history")
def history():
    return jsonify(service.get_history())


if __name__ == "__main__":
    app.run(debug=True)
