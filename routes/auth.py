from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
import json
from settings import db, security
from model import User
import jwt
import pytz


class ViewAuth(Resource):
    @staticmethod
    def post():
        tz = pytz.timezone('America/Sao_Paulo')
        user = User()
        if 'password' and 'username' in request.json:
            query_user = user.query.filter_by(username=request.json['username']).first_or_404()
            if query_user.verifyPassword(request.json['password']):
                j_user = user.to_json(query_user)
                payload = {"id": j_user['id'],
                           "exp": datetime.now().astimezone(tz) + timedelta(minutes=7)
                           }
                token = jwt.encode(payload, security.SECRET_KEY(), algorithm="HS256")
                return {'user': query_user.__repr__(), 'token': token}, 200
            else:
                return 'Usuário não autenticado', 403
        else:
            return 'Informe o usuário e senha', 401
