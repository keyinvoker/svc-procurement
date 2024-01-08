from flask import Blueprint
from flask_restful import Api

from eproc.resources.petty_cash_claim import PettyCashClaimResource

petty_cash_claim_blueprint = Blueprint("petty_cash_claim_blueprint", __name__, url_prefix="/petty-cash-claim")
petty_cash_claim_api = Api(petty_cash_claim_blueprint)
petty_cash_claim_api.add_resource(PettyCashClaimResource, "")
