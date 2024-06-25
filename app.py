from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_cors import CORS

pymysql.install_as_MySQLdb()
import MySQLdb
#import config.config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    #TODO
    app.config.from_object('config.config.Config')
    db.init_app(app)

    with app.app_context():
        from routes.api_api import api_api
        app.register_blueprint(api_api, url_prefix='/api')
        from routes.api_materia import api_materia
        app.register_blueprint(api_materia, url_prefix='/api')
        from routes.api_nota import api_nota
        app.register_blueprint(api_nota, url_prefix='/api')
        # Creacion de tablas en la base de datos
        db.create_all()
    return app

