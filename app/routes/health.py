from flask import Blueprint, jsonify 

health_bp = Blueprint("health", __name__)

@health_bp.get("/health/live")
def live():
    return jsonify(status="alive")