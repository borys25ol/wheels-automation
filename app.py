import os

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from config import config_by_name
from spreadseet import GoogleSpreadsheetService

app = Flask(__name__)
CORS(app)

config_name = os.getenv("CONFIG") or "dev"

app.config.from_object(config_by_name[config_name])


@app.route("/api/roulette", methods=["POST"])
@cross_origin()
def add_number():
    content = request.json

    numbers, source = content["numbers"], content["source"]
    service = GoogleSpreadsheetService(sheet_name=app.config["SHEET_NAME"])

    added_numbers = service.append_data_row(values=numbers, column=source)
    total_numbers = service.get_column_data(column=source)

    return jsonify(
        success=True, added_numbers=len(added_numbers), total_numbers=len(total_numbers)
    )


if __name__ == "__main__":
    app.run(debug=True)
