import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # Configurações do banco de dados
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pizzaria.db")
    
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Fechamento de Caixa - Pizzaria"
    
    # Configurações de CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ]
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua-chave-secreta-aqui")
    
    # Configurações de paginação
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100

settings = Settings()
