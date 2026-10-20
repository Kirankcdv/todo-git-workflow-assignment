from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"


def load_items():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def home():
    return render_template("index.html", items=load_items())


@app.route("/api", methods=["GET"])
def api():
    return jsonify(load_items())


if __name__ == "__main__":
    app.run(debug=True)