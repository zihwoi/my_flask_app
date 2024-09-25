from . import db
from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    invite_code = db.Column(db.String(20), nullable=True)  # Invite code for registration

    entries = db.relationship('GratitudeEntry', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class GratitudeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create an instance of SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Define the name of the table

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    email = db.Column(db.String(150), unique=True, nullable=False)  # User's email
    password = db.Column(db.String(150), nullable=False)  # Hashed password

    def set_password(self, password):
        """Hash the password before storing it."""
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)    
