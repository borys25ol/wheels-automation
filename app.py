import os
from collections import defaultdict

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from config import config_by_name
from spreadseet import GoogleSpreadsheetService

app = Flask(__name__)
CORS(app)

config_name = os.getenv("CONFIG") or "dev"

app.config.from_object(config_by_name[config_name])

cached_numbers = defaultdict(list)


@app.route("/api/health-check")
def heal_check():
    return jsonify(success=True)


@app.route("/api/roulette", methods=["POST"])
@cross_origin()
def add_number():
    global cached_numbers

    content = request.json

    numbers, source = content["numbers"], content["source"]

    if len(cached_numbers[source]) == 0:
        cached_numbers[source] = numbers

    if cached_numbers[source] != numbers:
        app.logger.info("Changes in cache detected. Got new numbers.")

        service = GoogleSpreadsheetService(sheet_name=app.config["SHEET_NAME"][source])
        added_numbers = service.append_data_row(values=numbers, column=source)

        cached_numbers[source] = numbers

        return jsonify(success=True, added_numbers=len(added_numbers))
    else:
        app.logger.info("Got no new numbers from the website.")

        return jsonify(success=True, added_numbers=0)
