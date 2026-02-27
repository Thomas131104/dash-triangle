import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path="/history")


layout = dbc.Container([

    html.H2("📜 Tra cứu tam giác"),
    html.Hr(),

    dbc.Card([

        dbc.CardHeader(
            html.H5("🔎 Bộ lọc tra cứu")
        ),

        dbc.CardBody([
            # ===== ROW 1 =====
            dbc.Row([
                dbc.Col([
                    html.Label("Theo cạnh"),
                    dcc.Dropdown(
                        id="edge-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Tam giác đều","value":"Tam giác đều"},
                            {"label":"Tam giác cân","value":"Tam giác cân"},
                            {"label":"Tam giác thường","value":"Tam giác thường"}
                        ],
                        value="",
                        clearable=True
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Theo góc"),
                    dcc.Dropdown(
                        id="angle-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Tam giác nhọn","value":"Tam giác nhọn"},
                            {"label":"Tam giác vuông","value":"Tam giác vuông"},
                            {"label":"Tam giác tù","value":"Tam giác tù"}
                        ],
                        value="",
                        clearable=True
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Nguồn"),
                    dcc.Dropdown(

                        id="by-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Web","value":"web"},
                            {"label":"API","value":"api"}
                        ],
                        value="",
                        clearable=True
                    )
                ], md=4)
            ], className="mb-3"),



            # ===== ROW 2 =====
            dbc.Row([
                dbc.Col([
                    html.Label("Khoảng ngày"),
                    dcc.DatePickerRange(
                        id="date-filter"
                    )
                ], md=9),



                dbc.Col([
                    html.Br(),
                    dbc.Button(
                        "🔎 Tra cứu",
                        id="btn-search",
                        color="primary",
                        className="w-100"
                    )
                ], md=3)
            ])
        ])

    ], className="mb-4 shadow"),

    dcc.Loading(
        html.Div(id="table"),
        type="circle"
    )
])

@callback(
    Output("table","children"),
    Input("btn-search","n_clicks"),
    State("edge-filter","value"),
    State("angle-filter","value"),
    State("by-filter","value"),
    State("date-filter","start_date"),
    State("date-filter","end_date")
)
def search(n, edge_v, angle_v, by_v, start, end):

    if not n:
        return ""

    url = "http://127.0.0.1:8050/api/history"

    params = {
        "edge": edge_v,
        "angle": angle_v,
        "by": by_v,
        "start": start,
        "end": end
    }

    try:
        r = requests.get(url, params=params, timeout=5)

        if r.status_code != 200:
            return dbc.Alert(
                f"Lỗi API: {r.status_code}",
                color="danger"
            )

        response_json = r.json()

        if not response_json.get("success"):
            return dbc.Alert(
                "API trả về lỗi",
                color="warning"
            )

        data = response_json["data"]

    except requests.exceptions.RequestException as e:
        return dbc.Alert(
            f"Không kết nối được API: {e}",
            color="danger"
        )

    if not data:
        return dbc.Alert(
            "Không có dữ liệu phù hợp",
            color="info"
        )

    rows = []

    for i, t in enumerate(data, start=1):
        rows.append(
            html.Tr([
                html.Td(i),
                html.Td(t["edge_type"]),
                html.Td(t["angle_type"]),
                html.Td(t["by"]),
                html.Td(t["created_at"]),
                html.Td(f"({t['x1']},{t['y1']})"),
                html.Td(f"({t['x2']},{t['y2']})"),
                html.Td(f"({t['x3']},{t['y3']})")
            ])
        )

    return dbc.Table([
        html.Thead(
            html.Tr([
                html.Th("ID"),
                html.Th("Theo cạnh"),
                html.Th("Theo góc"),
                html.Th("Nguồn"),
                html.Th("Ngày"),
                html.Th("A"),
                html.Th("B"),
                html.Th("C")
            ])
        ),
        html.Tbody(rows)
    ],
    striped=True,
    bordered=True,
    hover=True)
