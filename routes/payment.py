from flask_restful import Resource
from flask import request
from datetime import datetime
import pytz
import json
from settings import db, security
from model import PaymentLog
from services import PagSeguro, jwt_required

class Payment(Resource):
    @staticmethod
    @jwt_required
    def post(current_user, id_cliente: int, id_compra: int):
        tz = pytz.timezone('America/Sao_Paulo')
        init = datetime.now().astimezone(tz)
        cliente = id_cliente
        compra = id_compra
        log: PaymentLog = PaymentLog()
        pagseguro: PagSeguro = PagSeguro('/charges', request.json)

        try:
            status, re = pagseguro.request('POST')
            end = datetime.now().astimezone(tz)
            diference: str = diferenceRequest(init, end)
            r = json.loads(re)
            if status == 200 or status == 201:
                uri_verify = '/charges/' + r['id']
                verify: PagSeguro = PagSeguro(uri_verify)
                status_v, re_v = verify.request('GET')
                r_v = json.loads(re_v)

                user_response = security.logPagseguro(int(r['payment_response']['code']))
                r_user = {
                    "id": r['id'].replace("CHAR_", ""),
                    "installments": r['payment_method']['installments'],
                    "try_payment": True,
                    "payment_response": user_response if user_response is not None else r['payment_response']
                }

                dict_log = {
                    'id_payment': r['id'].replace("CHAR_", ""),
                    'payment_request': str(request.json),
                    'payment_request_return': str(r),
                    'id_purchase': compra,
                    'id_client': cliente,
                    'date': init,
                    'http_status_code': status,
                    'solicitation_status': r['payment_response']['code'],
                    'payment_request_user_return': str(r_user),
                    'start_request_date': init,
                    'finish_request_date': end,
                    'request_duration_time': diference
                }
                log.to_obj(dict_log)
                db.session.add(log)
                db.session.commit()
                return r_user, status

            else:
                if int(r['error_messages'][0]['code']) == 40001 or int(r['error_messages'][0]['code']) == 40002 :
                    user_response = security.logPagseguro(int(r['error_messages'][0]['code']),
                                                          r['error_messages'][0]['parameter_name'])
                else:
                    user_response = security.logPagseguro(int(r['error_messages'][0]['code']))
                r_user = {
                    "id": None,
                    "installments": None,
                    "try_payment": False,
                    "payment_response": user_response if user_response is not None else r['payment_response']
                }
                dict_log = {
                    'id_payment': None,
                    'payment_request': str(request.json),
                    'payment_request_return': str(r),
                    'id_purchase': compra,
                    'id_client': cliente,
                    'date': init,
                    'http_status_code': status,
                    'solicitation_status': r['error_messages'][0]['code'] if r['error_messages'][0][
                        'code'] else 0000000,
                    'payment_request_user_return': str(r_user),
                    'start_request_date': init,
                    'finish_request_date': end,
                    'request_duration_time': diference
                }
                log.to_obj(dict_log)
                db.session.add(log)
                db.session.commit()
                return r_user, status
        except:
            end = datetime.now().astimezone(tz)
            diference: str = diferenceRequest(init, end)
            dict_log = {
                'id_payment': None,
                'payment_request': str(request.json),
                'payment_request_return': None,
                'id_purchase': compra,
                'id_client': cliente,
                'date': init,
                'http_status_code': None,
                'solicitation_status': None,
                'payment_request_user_return': 'Payment not made',
                'start_request_date': init,
                'finish_request_date': end,
                'request_duration_time': diference
            }
            log.to_obj(dict_log)
            db.session.add(log)
            db.session.commit()
            return 'INTERNAL_SERVER_ERROR', 500


def diferenceRequest(init, end):
    r = f' {end.year - init.year} years {end.month - init.month} months {end.day - init.day} days' \
        f' {end.hour - init.hour} hours {end.minute - init.minute} minutes' \
        f' {end.second - init.second} seconds {end.microsecond - init.microsecond} microseconds'
    return r
