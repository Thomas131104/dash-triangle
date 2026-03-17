from dash import html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import math
from __hidden.__solve import _solve_ccc_common


layout = html.Div([
    dbc.Container([

        dbc.Row([
            dbc.Col("Nhập góc (độ)", width=3),
            dbc.Col(width=9),
        ], className="fw-bold mb-3"),

        # Góc 1
        dbc.Row([
            dbc.Col("Góc 1 (độ)", width=3),
            dbc.Col(dbc.Input(id="gcg_angle1", type="number", value=45, className="mb-2"), width=9),
        ], className="mb-2"),

        # Cạnh giữa
        dbc.Row([
            dbc.Col("Cạnh giữa (x = a + b√c)", width=3),
            dbc.Col(dbc.Input(id="gcg_c_a", type="number", value=0, className="mb-2"), width=3),
            dbc.Col(dbc.Input(id="gcg_c_b", type="number", value=0, className="mb-2"), width=3),
            dbc.Col(dbc.Input(id="gcg_c_c", type="number", value=1, min=0, className="mb-2"), width=3),
        ], className="mb-2"),

        # Góc 2
        dbc.Row([
            dbc.Col("Góc 2 (độ)", width=3),
            dbc.Col(dbc.Input(id="gcg_angle2", type="number", value=45, className="mb-2"), width=9),
        ], className="mb-2"),

    ]),

    dbc.Row(
        dbc.Col(
            dcc.Loading(
                type="circle",
                children=dbc.Button(
                    "Tính",
                    id="btn_gcg",
                    color="primary",
                    className="mt-3"
                )
            ),
            width=12,
            className="text-center"
        )
    ),

    dbc.Row([
        dbc.Col(html.Div(id="o_gcg"), width=4),
        dbc.Col(dcc.Graph(id="output_gcg"), width=8)
    ])
],
id="gcg"
)

@callback(
    [
        Output("o_gcg", "children"),
        Output("output_gcg", "figure"),
    ],
    Input("btn_gcg", "n_clicks"),

    [
        State("gcg_angle1", "value"),
        State("gcg_c_a", "value"),
        State("gcg_c_b", "value"),
        State("gcg_c_c", "value"),
        State("gcg_angle2", "value"),
    ],
    prevent_initial_call=True
)
def calc_gcg(n, angle1_deg, c_a, c_b, c_c, angle2_deg):
    if None in [angle1_deg, c_a, c_b, c_c, angle2_deg]:
        raise PreventUpdate

    base = c_a + c_b * math.sqrt(max(c_c, 0))
    A = math.radians(angle1_deg)
    B = math.radians(angle2_deg)
    
    C_rad = math.pi - A - B
    sin_C = math.sin(C_rad)
    
    if abs(sin_C) < 1e-9:
        side1, side2 = 0.0, 0.0
    else:
        side1 = abs(base * math.sin(B) / sin_C)
        side2 = abs(base * math.sin(A) / sin_C)

    table, graph = _solve_ccc_common(side1, side2, base)

    if angle1_deg <= 0 or angle2_deg <= 0 or (angle1_deg + angle2_deg) >= 180 or base <= 0:
        return dbc.Alert("Dữ liệu không tạo thành tam giác (Tổng góc >= 180° hoặc cạnh <= 0)", color="danger"), None

    return table, graph