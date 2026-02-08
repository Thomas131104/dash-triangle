from dash import html, dcc, Input, Output, State 
import dash_bootstrap_components as dbc
from server import app
import triangle
import init_database

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
                html.Td(dcc.Input(id="x1", type="number")),
                html.Td(dcc.Input(id="y1", type="number")),
            ]),
            html.Tr([
                html.Td("Cạnh 2"),
                html.Td(dcc.Input(id="x2", type="number")),
                html.Td(dcc.Input(id="y2", type="number")),
            ]),
            html.Tr([
                html.Td("Cạnh 3"),
                html.Td(dcc.Input(id="x3", type="number")),
                html.Td(dcc.Input(id="y3", type="number")),
            ]),
        ])
    ],
    bordered=True,
)




app.layout = html.Div([
    html.Header(
        html.P("Chương trình tính thông số hình tam giác")
    ), 

    html.Main([
        input_form, 
        html.Button("Tính!", id = "btn_clicks"),
        html.Div(id = "output")
    ]),

    html.Footer(
        html.P("By Mus")
    )
])

@app.callback(
    Output("output", "children"),
    Input("btn_clicks", "n_clicks"),
    State("x1", "value"),
    State("y1", "value"),
    State("x2", "value"),
    State("y2", "value"),
    State("x3", "value"),
    State("y3", "value"),
)
def calculate_triangle(n_clicks, x1, y1, x2, y2, x3, y3):
    if n_clicks == 0:
        return "Nhập 3 cạnh rồi bấm Tính"

    if any(v is None for v in [x1, y1, x2, y2, x3, y3]):
        return "Nhập thiếu tọa độ"

    A = triangle.Point(x1, y1)
    B = triangle.Point(x2, y2)
    C = triangle.Point(x3, y3)

    AB = A.distance_to_other(B)
    AC = A.distance_to_other(C)
    BC = B.distance_to_other(C)

    tri = triangle.Triangle(AB, AC, BC)

    if not tri.is_exist():
        return "Ba điểm không tạo thành tam giác"

    record = init_database.TriangleDomain(
        x1 = x1, y1 = y1,
        x2 = x2, y2 = y2,
        x3 = x3, y3 = y3,
    )
    
    with init_database.get_session() as session:
        session.add(record)
        session.commit()


    return dbc.Table(
        [
            html.Thead(
                html.Tr([html.Th("Thông số"), html.Th("Giá trị")])
            ),
            html.Tbody([
                html.Tr([html.Td("AB"), html.Td(f"{AB:.2f}")]),
                html.Tr([html.Td("AC"), html.Td(f"{AC:.2f}")]),
                html.Tr([html.Td("BC"), html.Td(f"{BC:.2f}")]),
                html.Tr([html.Td("Chu vi"), html.Td(f"{tri.perimeter():.2f}")]),
                html.Tr([html.Td("Diện tích"), html.Td(f"{tri.area():.2f}")]),
            ])
        ],
        bordered=True,
        striped=True,
        hover=True
    )

    

if __name__ == "__main__":
    app.run()