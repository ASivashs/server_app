from flask import jsonify, request, Blueprint

from datetime import datetime
from bson.errors import InvalidId
from bson import ObjectId

from mongodb_config import collections
from validator import validate_data
from utils import MongoJSONEncoder


reports = Blueprint("reports", __name__)


@reports.route("/", methods=["GET"])
def get_reports():
    data = [field for field in collections.find()]
    return jsonify(MongoJSONEncoder().encode(data)), 200


@reports.route("/<key>", methods=["GET"])
def get_report_by_id(key):
    data = collections.find_one({"key": key})
    if data:
        return jsonify({
            "key": data["key"],
            "value": data["value"]
            }), 200
    return jsonify({
        "error": "Key not found",
    }), 404


@reports.route("/", methods=["POST"])
def create_report():
    
    validate_result = validate_data(request=request)
    
    if validate_result is True:
        create_data = request.json
        create_data["time"] = datetime.now()
        collections.insert_one(create_data)
        return jsonify(MongoJSONEncoder().encode(create_data))
    return jsonify(MongoJSONEncoder().encode(validate_result))


@reports.route("/", methods=["PUT"])
def update_report():
    validate_result = validate_data(request=request)
    
    try:
        reqId = ObjectId(request.json.get('_id'))
    except InvalidId as ex:
        return jsonify(
            {
                "invalid id" : f"{ex}"
            })
    
    if validate_result is True:
        create_data = request.json
        create_data.pop("_id")
        query = {"_id" : reqId}
        newValue = {"$set" : convertedRequest}
        collections.update_many(query, newValue)
        return jsonify(MongoJSONEncoder().encode(query))
    return jsonify(MongoJSONEncoder().encode(validate_result))
    