from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from api.triangle_api import triangle_bp
from api.history_api import history_bp
from layout import layout

from flasgger import Swagger
import yaml

load_figure_template("lux")

# ===== Flask server =====
server = Flask(__name__)


# ===== Register API =====
server.register_blueprint(triangle_bp)
server.register_blueprint(history_bp)


# ===== Swagger =====
with open("swagger.yaml", encoding="utf-8") as f:
    template = yaml.safe_load(f)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(server, template=template, config=swagger_config)




# ===== Dash app =====
app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    suppress_callback_exceptions=True,
    update_title=None,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Công cụ tính toán và vẽ tam giác thông minh"},
        {"name": "keywords", "content": "triangle, geometry, plotly, dash, euler line, circumcircle"},
        {"rel": "icon", "type": "image/png", "href": "/static/images/favicon.png"},
        {"name": "author", "content": "Mus"}
    ]
)

app.title = "Triangle Analyzer"
app.layout = layout
