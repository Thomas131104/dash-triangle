from flask import jsonify, request
from server import server
import triangle
import init_database
from datetime import datetime

@server.route("/api/info")
def info():
    return jsonify(
        name="Triangle Calculator",
        author="Mus",
        version="1.0",
        message="Thanks for using this program",
        today=datetime.now().isoformat()
    )


@server.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json(force=True)
    x1 = data.get("x1", 0)
    y1 = data.get("y1", 0)
    x2 = data.get("x2", 0)
    y2 = data.get("y2", 0)
    x3 = data.get("x3", 0)
    y3 = data.get("y3", 0)

    if any(v is None for v in [x1, y1, x2, y2, x3, y3]):
        return jsonify({
            "message" : "Nhập thiếu tọa độ",
            "today" : datetime.now().isoformat(),
            "data" : None
        }), 400
    
    try:
        x1, y1, x2, y2, x3, y3 = map(float, [x1, y1, x2, y2, x3, y3])
    except (TypeError, ValueError):
        return jsonify({
            "message": "Tọa độ phải là số",
            "data": None
        }), 400


    A = triangle.Point(x1, y1)
    B = triangle.Point(x2, y2)
    C = triangle.Point(x3, y3)

    AB = A.distance_to_other(B)
    AC = A.distance_to_other(C)
    BC = B.distance_to_other(C)

    tri = triangle.Triangle(AB, AC, BC)

    if not tri.is_exist():
        return jsonify({
            "message" : "Tam giác này không tồn tại",
            "today" : datetime.now().isoformat(),
            "data" : None
        }), 400

    record = init_database.TriangleDomain(
        x1 = x1, y1 = y1,
        x2 = x2, y2 = y2,
        x3 = x3, y3 = y3,
        by = "web"
    )
    
    try:
        with init_database.get_session() as session:
            session.add(record)
            session.commit()
    except Exception as e:
        return jsonify({
            "message": "Lỗi lưu DB",
            "error": str(e)
        }), 500


    return jsonify({
        "message" : "Các giá trị",
        "today" : datetime.now().isoformat(),
        "data" : {
            "perimeter" : tri.perimeter(),
            "area" : tri.area(),
            "incircle_radius" : tri.incircle_radius(),
            "circumcircle_radius" : tri.circumcircle_radius(),
        }
    })