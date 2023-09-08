from logging import getLogger
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from procurement.config import APP_NAME, Config

app_logger = getLogger("app")
error_logger = getLogger("error")

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(APP_NAME)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)
        migrate.init_app(app, db)

        from procurement.blueprints.healthz import healthz_blueprint
        from procurement.blueprints.auth import auth_blueprint
        app.register_blueprint(healthz_blueprint)
        app.register_blueprint(auth_blueprint)

        print(f"\nEndpoints:")
        for api in app.url_map.iter_rules():
            if api.endpoint == "static":
                continue
            print(f"- {api.rule} <{api.endpoint}>")
        print()

        return app
