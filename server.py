from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

from api.triangle_api import triangle_bp
from api.history_api import history_bp

from flasgger import Swagger
import yaml

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
    suppress_callback_exceptions=True
)

app.title = "My web"
