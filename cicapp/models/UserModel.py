from . import db,bcrypt
from datetime import datetime


class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    created_date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow())
    modified_at =  db.Column(db.DateTime,nullable=False, default=datetime.utcnow())

    def __init__(self, data):
        self.username = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.created_date = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def update(self, data):
        for key, item in data.items():
            if key == 'password': # add this new line
                self.password = self.__generate_hash(value) # add this new line
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()
    
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
