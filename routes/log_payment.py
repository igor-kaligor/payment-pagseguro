from flask_restful import Resource
import json
from model import PaymentLog
from services import PagSeguro, jwt_required


class LogPayment(Resource):
    @staticmethod
    @jwt_required
    def get(current_user, id_compra: int):
        compra = id_compra
        log: PaymentLog = PaymentLog()
        dto_log = log.query.filter_by(id_purchase=compra).first()
        data_log = log.to_json(dto_log)
        if data_log['id_payment']:
            paglog: PagSeguro = PagSeguro('/charges/'+data_log['id_payment'])
            status, re = paglog.request('GET')
            r = json.loads(re)
            return r, status
        else:
            return 'COMPRA NÃO REALIZADA', 500
