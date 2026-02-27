from flask import jsonify
from datetime import datetime

def success(data):
    return jsonify({
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "data": data
    })


def error(message, code=400):
    return jsonify({
        "success": False,
        "timestamp": datetime.now().isoformat(),
        "error": message
    }), code