from dash import html, dcc
import dash_bootstrap_components as dbc
import numpy as np
from triangle import TriangleWithCoords

def _create_table(x1, y1, x2, y2, x3, y3):
    tri = TriangleWithCoords(x1, y1, x2, y2, x3, y3)
    edges = tri.triangle_edges
    angles = edges.angles()

    return dbc.Table(
        [
            html.Thead(html.Tr([
                html.Th("Thông số"),
                html.Th("Giá trị")
            ])),
            html.Tbody([
                html.Tr([html.Td("Cạnh a (BC)"), html.Td(f"{edges.a:.2f}")]),
                html.Tr([html.Td("Cạnh b (AC)"), html.Td(f"{edges.b:.2f}")]),
                html.Tr([html.Td("Cạnh c (AB)"), html.Td(f"{edges.c:.2f}")]),
                html.Tr([html.Td("Loại tam giác"), html.Td(edges.triangle_type())]),
                html.Tr([html.Td("Góc A"), html.Td(f"{np.degrees(angles['angle_a']):.2f}")]),
                html.Tr([html.Td("Góc B"), html.Td(f"{np.degrees(angles['angle_b']):.2f}")]),
                html.Tr([html.Td("Góc C"), html.Td(f"{np.degrees(angles['angle_c']):.2f}")]),
                html.Tr([html.Td("Chu vi"), html.Td(f"{edges.perimeter():.2f}")]),
                html.Tr([html.Td("Diện tích"), html.Td(f"{edges.area():.2f}")]),
                html.Tr([html.Td("Bán kính nội tiếp"), html.Td(f"{edges.incircle_radius():.2f}")]),
                html.Tr([html.Td("Bán kính ngoại tiếp"), html.Td(f"{edges.circumcircle_radius():.2f}")]),
            ])
        ],
        bordered=True,
        striped=True,
        hover=True
    )
