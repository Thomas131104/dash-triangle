from dash import Dash, html, dcc 

app = Dash(__name__)

app.title = "My web"
server = app.server