from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel
from ..shared.Authentication import Auth
from cicapp.schemas.user import validate_user

user_api = Blueprint('user_api', __name__)


@user_api.route("/login", methods=['POST'])
def login():
    data = validate_user(request.get_json())
    if data['ok']:
        email_ = request.get_json()['email']
        password_ = request.get_json()['password']
        user = UserModel.query.filter_by(email=email_).first()
        if user and bcrypt.check_password_hash(user.password, password_):
            del password_
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token

            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
