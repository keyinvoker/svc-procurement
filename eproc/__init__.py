from logging import getLogger
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from eproc.config import APP_NAME, Config

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

        from eproc.blueprints.auth import auth_blueprint
        from eproc.blueprints.budget import budget_blueprint
        from eproc.blueprints.company import company_blueprint
        from eproc.blueprints.cost_center import cost_center_blueprint
        from eproc.blueprints.dashboard import dashboard_blueprint
        from eproc.blueprints.healthz import healthz_blueprint
        from eproc.blueprints.invoice import invoice_blueprint
        from eproc.blueprints.item import item_blueprint
        from eproc.blueprints.link import link_blueprint
        from eproc.blueprints.procurement_request import procurement_request_blueprint
        from eproc.blueprints.price_comparison import price_comparison_blueprint
        from eproc.blueprints.purchase_order import purchase_order_blueprint
        from eproc.blueprints.procurement_request_progress import procurement_request_progress_blueprint
        from eproc.blueprints.system_config import system_config_blueprint
        from eproc.blueprints.user.employee import employee_blueprint
        from eproc.blueprints.user.user import user_blueprint
        from eproc.blueprints.vendor import vendor_blueprint
        from eproc.blueprints.vendor_rfq import vendor_rfq_blueprint
        app.register_blueprint(healthz_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(dashboard_blueprint)
        app.register_blueprint(procurement_request_blueprint)
        app.register_blueprint(vendor_rfq_blueprint)
        app.register_blueprint(price_comparison_blueprint)
        app.register_blueprint(purchase_order_blueprint)
        app.register_blueprint(procurement_request_progress_blueprint)
        app.register_blueprint(invoice_blueprint)
        app.register_blueprint(company_blueprint)
        app.register_blueprint(user_blueprint)
        app.register_blueprint(employee_blueprint)
        app.register_blueprint(vendor_blueprint)
        app.register_blueprint(budget_blueprint)
        app.register_blueprint(cost_center_blueprint)
        app.register_blueprint(item_blueprint)
        app.register_blueprint(link_blueprint)
        app.register_blueprint(system_config_blueprint)

        print_all_endpoints = False
        if print_all_endpoints:
            print(f"\nEndpoints:")
            for api in app.url_map.iter_rules():
                if api.endpoint == "static":
                    continue
                api.methods.difference_update({'HEAD', 'OPTIONS'})
                print(f"{api.rule}: {api.methods}")
            print()

        return app
