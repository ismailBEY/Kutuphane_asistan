from flask import Flask, render_template
from flasgger import Swagger
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    # template_folder='templates' diyerek yerini garantiye alıyoruz
    app = Flask(__name__, template_folder='templates') 
    
    # --- KONFIGURASYON ---
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    if not app.config['SQLALCHEMY_DATABASE_URI']:
         raise RuntimeError("DATABASE_URL environment variable is not set")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Guvenlik icin degistirilmeli
    
    db.init_app(app)
    jwt.init_app(app)

    CORS(app)
    
    Swagger(app, template_file='swagger.yaml')

    # Blueprint'leri burada import ediyoruz (Circular import'u onlemek icin)
    from .blueprints.books import books_bp
    from .blueprints.auth import auth_bp
    
    app.register_blueprint(books_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Veritabanını oluştur
    with app.app_context():
        from . import models
        db.create_all()

    # --- ANA SAYFA ---
    @app.route('/')
    def index():
        return render_template('index.html')
    # -----------------

    return app
