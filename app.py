from flask import Flask, jsonify, request, json
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xf2VW3xcWshyUSmlIjcGjUUzeF7nKq'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:cicapp_postgres@localhost:5432/test'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'xf2VW3xcasdasdWshyUSmlIjcGjUUzeF7nKq'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

@app.route('/users/register', methods=['POST'])
def register():
    user_name = request.get_json()['user_name']
    email_ = request.get_json()['email']
    password_ = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created_ = datetime.utcnow()
	
    db.session.add(User(username=user_name,email=email_,password=password_,created=created_))
    mysql.connection.commit()
	
    result = {
		'user_name' : user_name,
		'email' : email,
		'password' : password,
		'created' : created
	}

    return jsonify({'result' : result})
	