from flask import jsonify,request, json, Response, Blueprint, g
from ..models.UserModel import UserModel,bcrypt,datetime,db
from ..shared.Authentication import Auth
from ..schemas.user import validate_user

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

@user_api.route('/register', methods=['POST'])
def create():
    """
    Create User Function
    """
    req_data = request.get_json()
    data = validate_user(req_data)
    if data['ok']:
        print("Json Validation is OK")
        # check if user already exist in the db
        user_in_db = UserModel.get_user_by_email(req_data.get('user_name'))
        print(user_in_db)
        if user_in_db:
            message = {'error': 'User already exist, please supply another user name'}
            return custom_response(message, 400)
        
        if UserModel.get_user_by_username(req_data.get('email')):
            message = {'error': 'User already exist, please supply another user name'}
            return custom_response(message, 400)
        
        user = UserModel(req_data)
        user.save()
        token = Auth.generate_token(req_data.get('id'))
        return custom_response({'jwt_token': token}, 201)
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(req_data['message'])}), 400

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

'''
@user_api.route('/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        user_name = request.get_json()['user_name']
        email_ = request.get_json()['email']
        password_ = bcrypt.generate_password_hash(
            request.get_json()['password']).decode('utf-8')
        created_ = datetime.utcnow()

        if UserModel.query.filter_by(username=user_name).first():
            return jsonify({'result': "A felhasználónév már foglalt"})

        if UserModel.query.filter_by(email=email_).first():
            return jsonify({'result': "Az email már foglalt"})

        db.session.add(
            UserModel(name=user_name, email=email_, password=password_))
        db.session.commit()

        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
        '''