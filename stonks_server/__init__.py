from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

# # i used this : https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

# initiate SQLAlchemy so that we can use it later in our models
#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
   # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://db.sqlite'
   # db.init_app(app)
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
