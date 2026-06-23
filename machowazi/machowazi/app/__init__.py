import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///machowazi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail config
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@machowazi.co.ke')

    # Upload config
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please sign in to write a review.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.reviews import reviews_bp
    from .routes.companies import companies_bp
    from .routes.salaries import salaries_bp
    from .routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(companies_bp, url_prefix='/companies')
    app.register_blueprint(salaries_bp, url_prefix='/salaries')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create tables
    with app.app_context():
        db.create_all()
        from .seed import seed_data
        seed_data()

    return app
