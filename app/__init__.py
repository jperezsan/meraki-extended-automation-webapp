from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app import organization_data
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints for modules
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .sdwan import sdwan as sdwan_blueprint
    app.register_blueprint(sdwan_blueprint, url_prefix='/sdwan')

    # Initialize organization data
    organization_data.init()

    return app