import jwt
import os
import datetime
from flask import json
from cicapp.models import UserModel


class Auth():
  @staticmethod
  def generate_token(user_id):
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
      }
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating user token'}),
        status=400
      )

  @staticmethod
  def decode_token(token):
    re = {'data': {}, 'error': {}}
    try:
      payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
      re['data'] = {'user_id': payload['sub']}
      return re
    except jwt.ExpiredSignatureError as e1:
      re['error'] = {'message': 'token expired, please login again'}
      return re
    except jwt.InvalidTokenError:
      re['error'] = {'message': 'Invalid token, please try again with a new token'}
      return re
