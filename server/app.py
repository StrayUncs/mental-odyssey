from flask import Flask


app = Flask(__name__)

@app.route("/main-room")
def index():
    return {"main": "room"}


if __name__ == "__main__":
    app.run(debug=True)
