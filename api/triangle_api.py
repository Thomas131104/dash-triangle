from flask import Blueprint,request,jsonify
from api.helper import success,error
from api.service import *


triangle_bp=Blueprint(
    "triangle",
    __name__,
    url_prefix="/api"
)

@triangle_bp.route("/info")
def info():
    return jsonify(
        name="Triangle Calculator",
        version="1.0"
    )


@triangle_bp.route("/calculate/coords", methods=["POST"])
def coords():

    data=request.get_json()

    try:
        x1=float(data["x1"])
        y1=float(data["y1"])

        x2=float(data["x2"])
        y2=float(data["y2"])

        x3=float(data["x3"])
        y3=float(data["y3"])
    except:
        return error("Input sai")


    tri=triangle_from_coords(
        x1,y1,x2,y2,x3,y3
    )

    try:
        result=analyze_triangle(tri)
    except:
        return error("Tam giác sai")
    return success(result)


@triangle_bp.route("/calculate/edge/ccc", methods=["POST"])
def calculate_ccc():

    data = request.get_json()

    try:
        a = float(data["edge_1"])
        b = float(data["edge_2"])
        c = float(data["edge_3"])
    except (KeyError, TypeError, ValueError):
        return error("Input sai")

    try:
        tri = triangle_ccc(a, b, c)
        result = analyze_triangle(tri)
    except ValueError as e:
        return error(str(e))

    return success(result)


@triangle_bp.route("/calculate/edge/cgc", methods=["POST"])
def calculate_cgc():

    data = request.get_json()

    try:
        a = float(data["edge_1"])
        b = float(data["edge_2"])
        angleC = float(data["angle_C"])
    except (KeyError, TypeError, ValueError):
        return error("Input sai")

    try:
        tri = triangle_cgc(a, b, angleC)
        result = analyze_triangle(tri)
    except ValueError as e:
        return error(str(e))

    return success(result)


@triangle_bp.route("/calculate/edge/gcg", methods=["POST"])
def calculate_gcg():

    data = request.get_json()

    try:
        A = float(data["angle_A"])
        c = float(data["edge"])
        B = float(data["angle_B"])
    except (KeyError, TypeError, ValueError):
        return error("Input sai")

    try:
        tri = triangle_gcg(A, c, B)
        result = analyze_triangle(tri)
    except ValueError as e:
        return error(str(e))

    return success(result)