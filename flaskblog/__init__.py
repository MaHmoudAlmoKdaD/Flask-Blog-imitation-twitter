
# Flask: to write flask code.
# render_template: to invoke the HTML template.
# url_for: uniform resourses location for any path .
# flash: messege(alert).
# redirect: redirect method in my file to run
from flask import Flask
# from my file forms import classes RegistrationForm, LoginForm
# from cmd to test:
# from flaskblog import db
# from flaskblog.models import User, Post

# db.create_all() # to create site.db
# User.query.all() # to show what we have in user table
# to add user from cmd:
# user_1 = User(username="mahmoud", email="me@gmail.com", password="pasword")
# db.session.add(user_1)
# User.query.all()
# user.query.first()
# to search about user by certain username:
# User.query.filter_by(username="mahmouda").all() / User.query.filter_by(username="mahmouda").first()
#  user_1.id
# user = User.query.get(1)
# user / then click enter # get the first user in user table
# db.session.commit()
from flask_sqlalchemy import SQLAlchemy

# import Bcrypt class to encrypt the password
# from cmd :
# from flask_bcrypt import Bcrypt
# b = Bcrypt()
# b.generate_password_hash(password)# returns byte
# to convert byte to string write:
# b.generate_password_hash(password).decode('utf-8') # returns the string
# password = 'hunter2'
# pw_hash = b.generate_password_hash(password).decode('utf-8')
# b.check_password_hash(pw_hash, password) # returns True

from flask_bcrypt import Bcrypt

# flask_login : to login and logout.
from flask_login import LoginManager

# 
from flask_mail import Mail
# import smtplib, smtpd

from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# 'users.login' : it is mean route login
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app