from flask import Flask, request, jsonify
from service import TicketBookingSystem

app = Flask(__name__)
system = TicketBookingSystem()

@app.route("/")
def index():
    return jsonify({"message": "Ticket Booking System is running!"})

@app.route("/book", methods=["POST"])
def book():
    data = request.get_json()
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name is required"}), 400
    result = system.book_ticket(name)
    return jsonify({"result": result})

@app.route("/cancel", methods=["POST"])
def cancel():
    data = request.get_json()
    seat = data.get("seat")
    if seat is None:
        return jsonify({"error": "Seat number is required"}), 400
    result = system.cancel_ticket(int(seat))
    return jsonify({"result": result})

@app.route("/undo", methods=["POST"])
def undo():
    result = system.undo_cancellation()
    return jsonify({"result": result})

@app.route("/seats", methods=["GET"])
def seats():
    result = system.show_seats()
    return jsonify({"seats": result})

@app.route("/waiting", methods=["GET"])
def waiting():
    result = system.show_waiting()
    return jsonify({"waiting": result})

if __name__ == "__main__":
    app.run(debug=True)
