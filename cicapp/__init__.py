import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xf2VW3xcWshyUSmlIjcGjUUzeF7nKq'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:cicapp_postgres@localhost:5432/test'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

app.config['JWT_SECRET_KEY'] = 'xf2VW3xcasdasdWshyUSmlIjcGjUUzeF7nKq'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)

from cicapp import routes