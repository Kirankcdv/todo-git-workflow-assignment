from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone
import os

app = Flask(__name__)

# Configure MONGO_URI in your environment before running the app.
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri) if mongo_uri else None
db = client["todo_database"] if client else None
items_collection = db["items"] if db is not None else None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName", "").strip()
    item_description = request.form.get("itemDescription", "").strip()

    if not item_name or not item_description:
        return jsonify({"error": "Item Name and Item Description are required"}), 400

    if items_collection is None:
        return jsonify({"error": "MongoDB is not configured. Set MONGO_URI."}), 500

    item = {
        "itemName": item_name,
        "itemDescription": item_description,
        "createdAt": datetime.now(timezone.utc)
    }

    result = items_collection.insert_one(item)
    item["_id"] = str(result.inserted_id)
    item["createdAt"] = item["createdAt"].isoformat()

    return jsonify({
        "message": "To-Do item saved successfully",
        "item": item
    }), 201


if __name__ == "__main__":
    app.run(debug=True)