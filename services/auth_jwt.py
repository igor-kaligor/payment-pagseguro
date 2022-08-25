from functools import wraps
import jwt
from flask import jsonify
from flask import request
from settings import security
from model import User


def jwt_required(f):
    @wraps(f)
    def wraper(*args, **kwargs):
        token = None
        user = User()
        if 'authorization' in request.headers:
            token = request.headers['authorization']
            if not token:
                return jsonify({"error": "SEM PERMISSÃO"}), 403
            else:
                if 'Bearer ' in token:
                    try:
                        str_token = token.replace('Bearer ', '')
                        decoded = jwt.decode(str_token, security.SECRET_KEY(), algorithms="HS256")
                        current_user = user.query.filter_by(id=decoded['id']).first()
                        return f(current_user=current_user, *args, **kwargs)
                    except:
                        return jsonify({"error": "TOKEN INVÁLIDO"}), 401

                return jsonify({"error": "TOKEN INVÁLIDO"}), 401
        else:
            return jsonify({"error": "TOKEN INVÁLIDO"}), 401

    return wraper
