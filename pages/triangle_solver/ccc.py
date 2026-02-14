from dash import html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import math
from __hidden.__solve import _solve_ccc_common

layout = html.Div([

    dbc.Container([

        dbc.Row([
            dbc.Col("Nhập dạng x = a + b√c", width=3),
            dbc.Col("Nhập a", width=3),
            dbc.Col("Nhập b", width=3),
            dbc.Col("Nhập c", width=3),
        ], className="fw-bold mb-3"),

        dbc.Row([
            dbc.Col("Cạnh 1", width=3),
            dbc.Col(dcc.Input(id="c1_a", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="c1_b", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="c1_c", type="number", value=1, min=0), width=3),
        ], className="mb-2"),

        dbc.Row([
            dbc.Col("Cạnh 2", width=3),
            dbc.Col(dcc.Input(id="c2_a", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="c2_b", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="c2_c", type="number", value=1, min=0), width=3),
        ], className="mb-2"),

        dbc.Row([
            dbc.Col("Cạnh 3", width=3),
            dbc.Col(dcc.Input(id="c3_a", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="c3_b", type="number", value=0), width=3),
            dbc.Col(dcc.Input(id="c3_c", type="number", value=1, min=0), width=3),
        ], className="mb-2"),

    ]),
    
    dbc.Row(
        dbc.Col(
            dcc.Loading(
                type="circle",
                children=dbc.Button(
                    "Tính",
                    id="btn",
                    color="primary",
                    className="mt-3"
                )
            ),
            width=12,
            className="text-center"
        )
    ),


    dbc.Row([
        dbc.Col(html.Div(id="o1"), width=4),
        dbc.Col(dcc.Graph(id="output1"), width=8)
    ])
    ],
    id="ccc"
)

@callback(
    [
        Output("o1", "children"),
        Output("output1", "figure"),
    ],
    Input("btn", "n_clicks"),

    [
        State("c1_a", "value"),
        State("c1_b", "value"),
        State("c1_c", "value"),
    
        State("c2_a", "value"),
        State("c2_b", "value"),
        State("c2_c", "value"),

        State("c3_a", "value"),
        State("c3_b", "value"),
        State("c3_c", "value"),
    ],
    prevent_initial_call=True
)
def calc_ccc(n, c1_a, c1_b, c1_c, c2_a, c2_b, c2_c, c3_a, c3_b, c3_c):
    if None in [c1_a, c1_b, c1_c, c2_a, c2_b, c2_c, c3_a, c3_b, c3_c]:
        raise PreventUpdate

    # tính giá trị thực
    c1 = c1_a + c1_b * math.sqrt(c1_c)
    c2 = c2_a + c2_b * math.sqrt(c2_c)
    c3 = c3_a + c3_b * math.sqrt(c3_c)

    # Tam giác không tồn tại
    if c1 + c2 <= c3 or c1 + c3 <= c2 or c2 + c3 <= c1:
        return (
            dbc.Alert(
                "Tam giác không tồn tại",
                color="danger",
                className="mt-3"
            ),
            None
        )
    return _solve_ccc_common(c1, c2, c3)