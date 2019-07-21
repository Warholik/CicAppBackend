from marshmallow import fields, Schema
from datetime import datetime
from . import db, bcrypt

pw_hash = bcrypt.generate_password_hash('hunter2')
print(bcrypt.check_password_hash(pw_hash, 'hunter2'))


class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())
    modified_at = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, data):
        self.username = data.get('user_name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.created_date = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':  # add this new line
                self.password = self.__generate_hash(
                    value)  # add this new line
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)
  
    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    @staticmethod
    def get_user_by_username(value):
        return UserModel.query.filter_by(username=value).first()



    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True)
  created_date = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)