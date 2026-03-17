import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
from sqlalchemy import and_, or_
from init_database import get_session, TriangleDomain

dash.register_page(__name__, path="/history")



layout = dbc.Container([
    html.H2("📜 Tra cứu tam giác", className="text-light mb-4"),
    html.Hr(style={"borderColor": "rgba(255,255,255,0.1)"}),

    dbc.Card([
        dbc.CardHeader(
            html.H5("🔎 Bộ lọc tra cứu", className="mb-0")
        ),
        dbc.CardBody([
            dbc.Col([
                html.Label("Trạng thái", className="small text-muted"),
                dcc.Dropdown(
                    id="valid-filter",
                    options=[
                        {"label": "Tất cả", "value": "all"},
                        {"label": "Hợp lệ", "value": "true"},
                        {"label": "Không hợp lệ", "value": "false"}
                    ],
                    value="all",
                    clearable=False,
                    className="dark-dropdown"
                )
            ], md=3),

            # ===== ROW 1 =====
            dbc.Row([
                dbc.Col([
                    html.Label("Theo cạnh", className="small text-muted"),
                    dcc.Dropdown(
                        id="edge-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Tam giác đều","value":"Tam giác đều"},
                            {"label":"Tam giác cân","value":"Tam giác cân"},
                            {"label":"Tam giác thường","value":"Tam giác thường"}
                        ],
                        value="",
                        clearable=True,
                        className="dark-dropdown" # Thêm class này
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Theo góc", className="small text-muted"),
                    dcc.Dropdown(
                        id="angle-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Tam giác nhọn","value":"Tam giác nhọn"},
                            {"label":"Tam giác vuông","value":"Tam giác vuông"},
                            {"label":"Tam giác tù","value":"Tam giác tù"}
                        ],
                        value="",
                        clearable=True,
                        className="dark-dropdown"
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Nguồn", className="small text-muted"),
                    dcc.Dropdown(
                        id="by-filter",
                        options=[
                            {"label":"Tất cả","value":""},
                            {"label":"Web","value":"web"},
                            {"label":"API","value":"api"}
                        ],
                        value="",
                        clearable=True,
                        className="dark-dropdown"
                    )
                ], md=4)
            ], className="mb-3"),

            # ===== ROW 2 =====
            dbc.Row([
                dbc.Col([
                    html.Label("Khoảng ngày", className="small text-muted d-block"),
                    dcc.DatePickerRange(
                        id="date-filter",
                        className="dark-date-picker" # Thêm class này
                    )
                ], md=9),

                dbc.Col([
                    html.Br(),
                    dbc.Button(
                        "🔎 Tra cứu",
                        id="btn-search",
                        color="primary",
                        className="w-100 shadow-sm"
                    )
                ], md=3)
            ])
        ])
    ], className="main-card mb-4 border-0"),

    dcc.Loading(
        html.Div(id="table-container"),
        type="circle",
        color="#4a90e2"
    )
], className="main-content g-4")



@callback(
    [Output("edge-filter", "disabled"),
     Output("angle-filter", "disabled"),
     Output("edge-filter", "value"),
     Output("angle-filter", "value")],
    Input("valid-filter", "value")
)
def toggle_dropdowns(valid_val):
    if valid_val == "false":
        return True, True, "", ""
    return False, False, dash.no_update, dash.no_update



@callback(
    Output("table-container", "children"),
    Input("btn-search", "n_clicks"),
    State("valid-filter", "value"),
    State("edge-filter", "value"),
    State("angle-filter", "value"),
    State("by-filter", "value"),
    State("date-filter", "start_date"),
    State("date-filter", "end_date")
)
def search(n, is_valid_v, edge_v, angle_v, by_v, start, end):
    if not n: return ""

    session = get_session()
    try:
        query = session.query(TriangleDomain)

        # 1. Lọc theo Trạng thái (Hợp lệ / Không hợp lệ)
        if is_valid_v != "all":
            is_valid_bool = True if is_valid_v == "true" else False
            query = query.filter(TriangleDomain.is_valid == is_valid_bool)

        # 2. Lọc theo Cạnh và Góc (ĐƯA RA NGOÀI khối IF ở trên)
        # Điều này giúp khi chọn "Tất cả", nếu Mus chọn thêm "Tam giác tù" 
        # thì kết quả sẽ lọc đúng những tam giác tù (và tự loại bỏ Invalid vì Invalid có Cạnh/Góc = None)
        if edge_v:
            query = query.filter(TriangleDomain.edge_type == edge_v)
        if angle_v:
            query = query.filter(TriangleDomain.angle_type == angle_v)
        
        # 3. Các bộ lọc khác
        if by_v: 
            query = query.filter(TriangleDomain.by == by_v)
        if start: 
            query = query.filter(TriangleDomain.created_at >= start)
        if end: 
            query = query.filter(TriangleDomain.created_at <= end)

        results = query.order_by(TriangleDomain.created_at.desc()).all()

        if not results:
            return dbc.Alert("Không có dữ liệu phù hợp.", color="info", className="mt-3")

        rows = []
        for i, t in enumerate(results, start=1):

            edge_display = dbc.Badge(t.edge_type, color="primary", pill=True) if t.is_valid else "---"
            angle_display = t.angle_type if t.is_valid else "---"
            status_badge = dbc.Badge(
                "Valid" if t.is_valid else "Invalid", 
                color="success" if t.is_valid else "danger"
            )

            rows.append(
                html.Tr([
                    html.Td(i),
                    html.Td(edge_display),   
                    html.Td(angle_display),  
                    html.Td(status_badge),  
                    html.Td(t.by.upper()),
                    html.Td(t.created_at.strftime("%Y-%m-%d %H:%M")),
                    html.Td(f"({t.x1:.4}, {t.y1:.4})", className="font-monospace small"),
                    html.Td(f"({t.x2:.4}, {t.y2:.4})", className="font-monospace small"),
                    html.Td(f"({t.x3:.4}, {t.y3:.4})", className="font-monospace small"),
                ])
            )


        return dbc.Table([
            html.Thead(html.Tr([
                html.Th("STT"), 
                html.Th("Loại cạnh"), 
                html.Th("Loại góc"), 
                html.Th("Trạng thái"),
                html.Th("Nguồn"), 
                html.Th("Thời gian"), 
                html.Th("Tọa độ A"), 
                html.Th("Tọa độ B"), 
                html.Th("Tọa độ C")
            ])),
            html.Tbody(rows)
        ], striped=True, hover=True, className="mt-3")

    except Exception as e:
        return dbc.Alert(f"Lỗi DB: {str(e)}", color="danger")
    finally:
        session.close()
