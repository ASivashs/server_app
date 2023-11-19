from flask import jsonify, request


def validate_data(request) -> dict | bool:

    if not request.data or not request.is_json:
        return jsonify(
            {
                "error" : "Incorrect data format."
            }
        )
    
    total = request.json.get("total", '')
    used = request.json.get("used", '')
    used_percentage = request.json.get("used_percentage", '')
    free = request.json.get("free", '')
    shared = request.json.get("shared", '')
    cache = request.json.get("cache", '')
    
    if not all((total, used, used_percentage, free, shared, cache)):
        return jsonify(
            {
                "error" : "Incorrect JSON headers."
            }
        )
    
    return True
