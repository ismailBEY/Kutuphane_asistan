from flask import Flask, render_template  # <-- render_template EKLENDI
from flasgger import Swagger
from flask_cors import CORS
from .blueprints.books import books_bp

def create_app():
    # template_folder='templates' diyerek yerini garantiye alıyoruz
    app = Flask(__name__, template_folder='templates') 
    CORS(app)
    
    app.config['SWAGGER'] = {
        'title': 'Library Assistant API',
        'uiversion': 3
    }
    Swagger(app)

    app.register_blueprint(books_bp, url_prefix='/api')

    # --- YENİ EKLENEN KISIM ---
    @app.route('/')
    def index():
        return render_template('index.html')
    # --------------------------

    return app
