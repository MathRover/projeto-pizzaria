"""
Configurações da aplicação
"""
import os

class Config:
    """Configurações base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui-mude-em-producao'
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'pizzaria.db')
    DEBUG = True

