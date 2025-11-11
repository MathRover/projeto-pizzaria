import os
from peewee import SqliteDatabase

# Caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'pizzaria.db')

# Criar diretório se não existir
os.makedirs(DATABASE_DIR, exist_ok=True)

# Criar instância do banco
db = SqliteDatabase(DATABASE_PATH)

def init_db():
    """Inicializa o banco de dados e cria as tabelas"""
    from .models import Despesa, Categoria
    
    db.connect()
    db.create_tables([Despesa, Categoria], safe=True)
    
    # Inserir categorias padrão se não existirem
    seed_categorias()
    
    return db

def close_db():
    """Fecha a conexão com o banco de dados"""
    if not db.is_closed():
        db.close()

def get_db():
    """Retorna a instância do banco de dados"""
    return db

def seed_categorias():
    """Insere categorias padrão no banco"""
    from .models import Categoria
    
    categorias_padrao = [
        {"nome": "Motoboys", "descricao": "Pagamentos para entregadores", "cor": "#28a745"},
        {"nome": "Boletos", "descricao": "Contas e boletos diversos", "cor": "#dc3545"},
        {"nome": "Impostos", "descricao": "Impostos e taxas", "cor": "#6f42c1"},
        {"nome": "Aluguel", "descricao": "Aluguel do imóvel", "cor": "#fd7e14"},
        {"nome": "Produtos", "descricao": "Compra de ingredientes e produtos", "cor": "#20c997"},
        {"nome": "Contas Fixas", "descricao": "Contas mensais fixas", "cor": "#17a2b8"},
        {"nome": "Internet", "descricao": "Internet e telefone", "cor": "#6c757d"},
        {"nome": "Salários", "descricao": "Pagamento de funcionários", "cor": "#ffc107"},
        {"nome": "Outros", "descricao": "Outras despesas diversas", "cor": "#6c757d"}
    ]
    
    for cat_data in categorias_padrao:
        Categoria.get_or_create(
            nome=cat_data["nome"],
            defaults={
                "descricao": cat_data["descricao"],
                "cor": cat_data["cor"]
            }
        )

