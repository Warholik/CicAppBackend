from flask import jsonify, request, json
from cicapp import app, db, bcrypt
from cicapp.modules import User
from cicapp.schemas import validate_user
from datetime import datetime
@app.route("/")
def home():
    return jsonify({'result': "Helloka"})


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

        db.session.add(User(username=user_name, email=email_, password=password_))
        db.session.commit()

        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route("/login",methods=['POST'])
def login():
    email_ = request.get_json()['email']
    password_ = request.get_json()['password']
    user = User.query.filter_by(email=email_).first()
    if user and bcrypt.check_password_hash(user.password, password_):
        return jsonify({'message': "You logged in!"})
    else:
        return jsonify({'message': "nem valid amit megadtál"})
