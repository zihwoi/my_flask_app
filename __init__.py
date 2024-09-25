from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create the Flask app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/zihwoi/Projects/my_flask_app/gratitude.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view (where unauthenticated users will be redirected)
login_manager.login_view = 'login'  # Make sure this matches the route name for your login view

# Import routes at the end to avoid circular imports
from . import routes

# User loader function
from .models import User  # Assuming User model is defined in models.py

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))