from dash import html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import math
from __hidden.__solve import _solve_ccc_common

layout = html.Div([

    dbc.Container([

        dbc.Row([
            dbc.Col("Nhập dạng cạnh = a + b√c", width=3),
            dbc.Col("Nhập a", width=3),
            dbc.Col("Nhập b", width=3),
            dbc.Col("Nhập c", width=3),
        ], className="fw-bold mb-3"),

        # Cạnh 1
        dbc.Row([
            dbc.Col("Cạnh 1", width=3),
            dbc.Col(dcc.Input(id="cgc_c1_a", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="cgc_c1_b", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="cgc_c1_c", type="number", value=1, min=0), width=3),
        ], className="mb-2"),

        # Góc giữa
        dbc.Row([
            dbc.Col("Góc giữa (độ)", width=3),
            dbc.Col(dcc.Input(id="cgc_angle", type="number", value=60), width=9),
        ], className="mb-2"),

        # Cạnh 2
        dbc.Row([
            dbc.Col("Cạnh 2", width=3),
            dbc.Col(dcc.Input(id="cgc_c2_a", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="cgc_c2_b", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="cgc_c2_c", type="number", value=1, min=0), width=3),
        ], className="mb-2"),

    ]),

    dbc.Row(
        dbc.Col(
            dcc.Loading(
                type="circle",
                children=dbc.Button(
                    "Tính",
                    id="btn_cgc",
                    color="primary",
                    className="mt-3"
                )
            ),
            width=12,
            className="text-center"
        )
    ),

    dbc.Row([
        dbc.Col(html.Div(id="o_cgc"), width=4),
        dbc.Col(dcc.Graph(id="output_cgc"), width=8)
    ])
],
id="cgc"
)


@callback(
    Output("output2", "figure"),
    Input("btn_cgc", "n_clicks"),
    State("cgc_c1", "value"),
    State("cgc_angle", "value"),
    State("cgc_c2", "value"),
    prevent_initial_call=True
)
@callback(
    [
        Output("o_cgc", "children"),
        Output("output_cgc", "figure"),
    ],
    Input("btn_cgc", "n_clicks"),

    [
        State("cgc_c1_a", "value"),
        State("cgc_c1_b", "value"),
        State("cgc_c1_c", "value"),

        State("cgc_angle", "value"),

        State("cgc_c2_a", "value"),
        State("cgc_c2_b", "value"),
        State("cgc_c2_c", "value"),
    ],
    prevent_initial_call=True
)
def calc_cgc(n, c1_a, c1_b, c1_c, angle_deg,
             c2_a, c2_b, c2_c):

    if None in [c1_a, c1_b, c1_c,
                angle_deg,
                c2_a, c2_b, c2_c]:
        raise PreventUpdate

    c1 = c1_a + c1_b * math.sqrt(c1_c)
    c2 = c2_a + c2_b * math.sqrt(c2_c)

    if angle_deg <= 0 or angle_deg >= 180:
        return dbc.Alert("Góc phải nằm giữa 0° và 180°", color="danger"), None

    angle = math.radians(angle_deg)

    # Định lý cos
    c3 = math.sqrt(c1**2 + c2**2 - 2*c1*c2*math.cos(angle))

    return _solve_ccc_common(c1, c3, c2)