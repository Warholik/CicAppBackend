from flask import jsonify, request, json
from datetime import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token,jwt_required, jwt_refresh_token_required, get_jwt_identity)
from cicapp import app, db, bcrypt
from cicapp.models import UserModel
from cicapp.schemas.user import validate_user


@app.route('/users/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        user_name = request.get_json()['user_name']
        email_ = request.get_json()['email']
        password_ = bcrypt.generate_password_hash(
            request.get_json()['password']).decode('utf-8')
        created_ = datetime.utcnow()

        if User.query.filter_by(username=user_name).first():
            return jsonify({'result': "A felhasználónév már foglalt"})

        if User.query.filter_by(email=email_).first():
            return jsonify({'result': "Az email már foglalt"})

        db.session.add(
            User(username=user_name, email=email_, password=password_))
        db.session.commit()

        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route("/login", methods=['POST'])
def login():
    data = validate_user(request.get_json())
    if data['ok']:
        email_ = request.get_json()['email']
        password_ = request.get_json()['password']
        user = User.query.filter_by(email=email_).first()
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


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200


@app.route('/user', methods=['GET', 'DELETE', 'PATCH'])
@jwt_required
def user():
    if request.method == 'GET':
        data = User.query.filter_by(username=data['email']).first()
        return jsonify({'ok': True, 'data': data}), 200
    data = request.json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
                db_response = User.query.filter_by(username=data['email']).first()
                if db_response:
                    db.session.delete(db_response)
                    db.session.commit()
                    response = {'ok': True, 'message': 'record deleted'}
                else:
                    response = {'ok': True, 'message': 'no record found'}
                return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
    if request.method == 'PATCH':

        return jsonify({'ok': True, 'message': 'record updated'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
