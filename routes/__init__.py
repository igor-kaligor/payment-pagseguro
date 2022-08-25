from flask import Blueprint
from flask_restful import Api
from .payment import Payment
from .auth import ViewAuth
from .log_payment import LogPayment
bp = Blueprint("api", __name__, url_prefix="")
api = Api(bp)


def init_app(app):
    api.add_resource(Payment, "/payment/<id_cliente>/<id_compra>")
    api.add_resource(LogPayment, "/payment/<id_compra>")
    api.add_resource(ViewAuth, "/token")

    app.register_blueprint(bp)
