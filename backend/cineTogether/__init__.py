# from dotenv import load_dotenv
# load_dotenv()  --> Buna artık gerek yok

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def createApp():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)

    return app
