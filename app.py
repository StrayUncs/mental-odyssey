from flask import Flask


app = Flask(__name__)

@app.route("/api")
def index():
    return {"index": "page"}


@app.route("/api/room/<int:room_id>")
def room(room_id):
    return {"room": room_id}


if __name__ == "__main__":
    app.run(debug=True)
