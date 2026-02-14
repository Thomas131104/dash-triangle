from dash import Dash, html, dcc
import dash_bootstrap_components as dbc 

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True)

app.title = "My web"
app_server = app.server

from triangle_api import triangle_bp

app_server.register_blueprint(triangle_bp)