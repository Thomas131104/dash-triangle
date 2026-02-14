from __hidden.__draw import _draw_triangle
from __hidden.__table import _create_table
from init_database import TriangleDomain, get_session
import triangle
from flask import jsonify
import datetime
import dash_bootstrap_components as dbc
import math

def _solve_ccc_common(a, b, c):

    if a + b <= c or a + c <= b or b + c <= a:
        return dbc.Alert("Tam giác không tồn tại", color="danger"), None

    x = (b**2 + c**2 - a**2) / (2*c)
    y = math.sqrt(max(b**2 - x**2, 0))

    graph = _draw_triangle(0, 0, c, 0, x, y)
    table = _create_table(0, 0, c, 0, x, y)

    domain = TriangleDomain(
        x1 = 0,
        y1 = 0,
        x2 = c,
        y2 = 0,
        x3 = x,
        y3 = y,
        by = "web"
    )

    with get_session() as session:
        try:
            session.add(domain)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)


    return table, graph
