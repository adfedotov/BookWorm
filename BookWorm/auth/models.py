from .. import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'USERS'

    uid = db.Column('UID', db.Integer, primary_key=True)
    first_name = db.Column('FName', db.String(50), nullable=False)
    last_name = db.Column('LName', db.String(50), nullable=False)
    email = db.Column('Email', db.String(320), nullable=False, unique=True, index=True)
    password = db.Column('Password', db.String(255), nullable=False)

    def __init__(self, first_name, last_name, email):
        """
        Constructor to create a user instance in the database

        :param first_name:
        :param last_name:
        :param email:
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return f'<User {self.email}>'

    def set_pass(self, password):
        """
        Sets user password by hashing it and adding to the database
        Separated from constructor because we should be able to set it
        without creating a new user

        :param password:
        """
        password_hash = generate_password_hash(password)
        self.password = password_hash

    def check_pass(self, password):
        """
        Checks whether provided password is the same as the actual one

        :param password:
        :rtype: bool
        """
        return check_password_hash(self.password, password)
