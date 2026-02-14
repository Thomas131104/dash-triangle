from flask import jsonify, request, Blueprint
import triangle
import init_database
import math
from datetime import datetime

triangle_bp = Blueprint("triangle", __name__, url_prefix="/api")

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

def analyze_triangle(tri):
    if not tri.is_exist():
        raise ValueError("Tam giác không tồn tại")

    return {
        "edge_1": tri.a,
        "edge_2": tri.b,
        "edge_3": tri.c,
        "perimeter": tri.perimeter(),
        "area": tri.area(),
        "incircle_radius": tri.incircle_radius(),
        "circumcircle_radius": tri.circumcircle_radius(),
    }


@triangle_bp.route("/api/info", methods=["POST", "GET"])
def info():
    return jsonify(
        name="Triangle Calculator",
        author="Mus",
        version="1.0",
        message="Thanks for using this program",
        today=datetime.now().isoformat()
    )


@triangle_bp.route("/calculate/coords", methods=["POST"])
def calculate_coords():
    data = request.get_json()
    if not data:
        return error("Request phải là JSON")

    try:
        x1, y1 = float(data["x1"]), float(data["y1"])
        x2, y2 = float(data["x2"]), float(data["y2"])
        x3, y3 = float(data["x3"]), float(data["y3"])
    except (KeyError, TypeError, ValueError):
        return error("Tọa độ không hợp lệ")

    A = triangle.Point(x1, y1)
    B = triangle.Point(x2, y2)
    C = triangle.Point(x3, y3)

    AB = A.distance_to_other(B)
    AC = A.distance_to_other(C)
    BC = B.distance_to_other(C)

    tri = triangle.Triangle(AB, AC, BC)

    try:
        result = analyze_triangle(tri)
    except ValueError:
        return error("Tam giác không tồn tại")

    # Lưu DB
    try:
        record = init_database.TriangleDomain(
            x1=x1, y1=y1,
            x2=x2, y2=y2,
            x3=x3, y3=y3,
            by="web"
        )

        with init_database.get_session() as session:
            session.add(record)
            session.commit()

    except Exception:
        return error("Lỗi lưu DB", 500)

    return success(result)


@triangle_bp.route("/calculate/edge/ccc", methods=["POST"])
def calculate_ccc():
    data = request.get_json()
    if not data:
        return error("Request phải là JSON")

    try:
        a = float(data["edge_1"])
        b = float(data["edge_2"])
        c = float(data["edge_3"])
    except (KeyError, TypeError, ValueError):
        return error("Cạnh không hợp lệ")

    tri = triangle.Triangle(a, b, c)

    try:
        result = analyze_triangle(tri)
        return success(result)
    except ValueError:
        return error("Tam giác không tồn tại")




@triangle_bp.route("/calculate/edge/cgc", methods=["POST"])
def calculate_cgc():
    data = request.get_json()
    if not data:
        return error("Request phải là JSON")

    try:
        a = float(data["edge_1"])
        b = float(data["edge_2"])
        angle_C = float(data["angle_C"])
    except (KeyError, TypeError, ValueError):
        return error("Dữ liệu không hợp lệ")

    # Định lý cos
    c = math.sqrt(a*a + b*b - 2*a*b*math.cos(angle_C))

    tri = triangle.Triangle(a, b, c)

    try:
        result = analyze_triangle(tri)
        return success(result)
    except ValueError:
        return error("Tam giác không tồn tại")




@triangle_bp.route("/calculate/edge/gcg", methods=["POST"])
def calculate_gcg():
    data = request.get_json()
    if not data:
        return error("Request phải là JSON")

    try:
        angle_A = float(data["angle_A"])
        c = float(data["edge"])
        angle_B = float(data["angle_B"])
    except (KeyError, TypeError, ValueError):
        return error("Dữ liệu không hợp lệ")

    angle_C = math.pi - angle_A - angle_B

    if angle_C <= 0:
        return error("Tổng hai góc phải nhỏ hơn π")

    # Định lý sin
    a = c * math.sin(angle_A) / math.sin(angle_C)
    b = c * math.sin(angle_B) / math.sin(angle_C)

    tri = triangle.Triangle(a, b, c)

    try:
        result = analyze_triangle(tri)
        return success(result)
    except ValueError:
        return error("Tam giác không tồn tại")
