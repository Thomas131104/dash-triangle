import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import numpy as np
from __hidden.__table import _create_table
import triangle
import init_database
from __hidden.__draw import _draw_triangle

dash.register_page(__name__, path="/calc/coord")

input_form = dbc.Table(
    [
        html.Thead(
            html.Tr([
                html.Th(""),
                html.Th("Theo trục x"),
                html.Th("Theo trục y"),
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Td("Cạnh 1"),
                html.Td(dcc.Input(id="x1", type="number", value=0)),
                html.Td(dcc.Input(id="y1", type="number", value=0)),
            ]),
            html.Tr([
                html.Td("Cạnh 2"),
                html.Td(dcc.Input(id="x2", type="number", value=0)),
                html.Td(dcc.Input(id="y2", type="number", value=0)),
            ]),
            html.Tr([
                html.Td("Cạnh 3"),
                html.Td(dcc.Input(id="x3", type="number", value=0)),
                html.Td(dcc.Input(id="y3", type="number", value=0)),
            ]),
        ])
    ],
    bordered=True,
)


layout = html.Div([
    input_form, 
    html.Button("Tính!", id="btn-calc"),

    dbc.Alert(
        id="alert",
        is_open=False,
        color="danger",
        dismissable=True
    ),

    dbc.Spinner(
        dbc.Row([
            dbc.Col(html.Div(id="output"), width=3),
            dbc.Col(dcc.Graph(id="triangle-graph"), width=9)
        ]),
        color="primary",
        type="border",
        fullscreen=False
    )
])


@callback(
    Output("output", "children"),
    Output("triangle-graph", "figure"),
    Output("alert", "children"),
    Output("alert", "is_open"),
    Input("btn-calc", "n_clicks"),
    State("x1", "value"), State("y1", "value"),
    State("x2", "value"), State("y2", "value"),
    State("x3", "value"), State("y3", "value"),
)
def calculate_triangle(n_clicks, x1, y1, x2, y2, x3, y3):
    if n_clicks is None:
        return None, None, None, False

    # 1️⃣ Validate input
    if any(v is None for v in [x1, y1, x2, y2, x3, y3]):
        return None, None, "Nhập thiếu tọa độ", True

    A = triangle.Point(x1, y1)
    B = triangle.Point(x2, y2)
    C = triangle.Point(x3, y3)

    AB = A.distance_to_other(B)
    AC = A.distance_to_other(C)
    BC = B.distance_to_other(C)

    tri = triangle.Triangle(AB, AC, BC)

    if not tri.is_exist():
        return None, {}, "Ba điểm không tạo thành tam giác", True

    # 2️⃣ Vẽ hình
    fig = _draw_triangle(x1, y1, x2, y2, x3, y3)

    # 3️⃣ Lưu DB
    record = init_database.TriangleDomain(
        x1=x1, y1=y1,
        x2=x2, y2=y2,
        x3=x3, y3=y3,
        by="web"
    )

    with init_database.get_session() as session:
        session.add(record)
        session.commit()

    # 4️⃣ Bảng kết quả
    table = _create_table(x1, y1, x2, y2, x3, y3)

    return table, fig, None, False