
import os
from flask import Flask
from database.db import init_db, close_db

def create_app():
    """Factory function para criar a aplicação Flask"""
    # Obter o diretório raiz do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-em-producao'
    app.config['DATABASE'] = 'database/pizzaria.db'
    
    # Inicializar banco de dados
    with app.app_context():
        init_db()
    
    # Registrar blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Fechar banco ao encerrar
    @app.teardown_appcontext
    def close_database(error):
        close_db()
    
    return app

