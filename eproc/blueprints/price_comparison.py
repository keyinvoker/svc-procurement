from flask import Blueprint
from flask_restful import Api

from eproc.resources.price_comparison import PriceComparisonResource

price_comparison_blueprint = Blueprint("price_comparison_blueprint", __name__, url_prefix="/price-comparison")

price_comparison_api = Api(price_comparison_blueprint)

price_comparison_api.add_resource(PriceComparisonResource, "")
