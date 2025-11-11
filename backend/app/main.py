from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from . import models, database
from pydantic import BaseModel
import sys
import os

# Adicionar o diretório pai ao path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

# Criar tabelas no banco
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Sistema de gerenciamento de despesas para pizzarias"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validação
class DespesaBase(BaseModel):
    descricao: str
    categoria: str
    valor: float
    data_vencimento: Optional[str] = None
    data_pagamento: Optional[str] = None
    observacoes: Optional[str] = None
    status: str = "pendente"

class DespesaCreate(DespesaBase):
    pass

class DespesaUpdate(BaseModel):
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    valor: Optional[float] = None
    data_vencimento: Optional[str] = None
    data_pagamento: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None

class Despesa(DespesaBase):
    id: int
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    cor: str = "#007bff"

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

class Estatisticas(BaseModel):
    total_despesas: int
    total_valor: float
    despesas_pendentes: int
    despesas_pagas: int

# Função para obter sessão do banco
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API da Pizzaria rodando 🚀"}

# Rotas para categorias
@app.get("/api/v1/categorias", response_model=List[Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    """Lista todas as categorias"""
    categorias = db.query(models.Categoria).all()
    return categorias

@app.post("/api/v1/categorias", response_model=Categoria, status_code=201)
def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Cria uma nova categoria"""
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Rotas para despesas
@app.get("/api/v1/despesas", response_model=List[Despesa])
def listar_despesas(db: Session = Depends(get_db)):
    """Lista todas as despesas"""
    despesas = db.query(models.Despesa).order_by(models.Despesa.created_at.desc()).all()
    return despesas

@app.post("/api/v1/despesas", response_model=Despesa, status_code=201)
def criar_despesa(despesa: DespesaCreate, db: Session = Depends(get_db)):
    """Cria uma nova despesa"""
    # Converter strings de data para objetos date
    despesa_data = despesa.dict()
    if despesa_data.get('data_vencimento'):
        despesa_data['data_vencimento'] = datetime.strptime(despesa_data['data_vencimento'], '%Y-%m-%d').date()
    if despesa_data.get('data_pagamento'):
        despesa_data['data_pagamento'] = datetime.strptime(despesa_data['data_pagamento'], '%Y-%m-%d').date()
    
    db_despesa = models.Despesa(**despesa_data)
    db.add(db_despesa)
    db.commit()
    db.refresh(db_despesa)
    return db_despesa

@app.get("/api/v1/despesas/{despesa_id}", response_model=Despesa)
def obter_despesa(despesa_id: int, db: Session = Depends(get_db)):
    """Obtém uma despesa específica"""
    despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return despesa

@app.put("/api/v1/despesas/{despesa_id}", response_model=Despesa)
def atualizar_despesa(despesa_id: int, despesa: DespesaUpdate, db: Session = Depends(get_db)):
    """Atualiza uma despesa existente"""
    db_despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if not db_despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    # Atualizar apenas os campos fornecidos
    update_data = despesa.dict(exclude_unset=True)
    
    # Converter strings de data para objetos date
    if 'data_vencimento' in update_data and update_data['data_vencimento']:
        update_data['data_vencimento'] = datetime.strptime(update_data['data_vencimento'], '%Y-%m-%d').date()
    if 'data_pagamento' in update_data and update_data['data_pagamento']:
        update_data['data_pagamento'] = datetime.strptime(update_data['data_pagamento'], '%Y-%m-%d').date()
    
    for field, value in update_data.items():
        setattr(db_despesa, field, value)
    
    db_despesa.updated_at = datetime.now()
    db.commit()
    db.refresh(db_despesa)
    return db_despesa

@app.delete("/api/v1/despesas/{despesa_id}")
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    """Deleta uma despesa"""
    db_despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if not db_despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    db.delete(db_despesa)
    db.commit()
    return {"message": "Despesa deletada com sucesso"}

@app.get("/api/v1/estatisticas", response_model=Estatisticas)
def obter_estatisticas(db: Session = Depends(get_db)):
    """Obtém estatísticas das despesas"""
    total_despesas = db.query(models.Despesa).count()
    total_valor = db.query(models.Despesa).with_entities(
        db.func.sum(models.Despesa.valor)
    ).scalar() or 0
    despesas_pendentes = db.query(models.Despesa).filter(
        models.Despesa.status == "pendente"
    ).count()
    despesas_pagas = db.query(models.Despesa).filter(
        models.Despesa.status == "pago"
    ).count()
    
    return Estatisticas(
        total_despesas=total_despesas,
        total_valor=float(total_valor),
        despesas_pendentes=despesas_pendentes,
        despesas_pagas=despesas_pagas
    )

# Rota para inserir categorias padrão
@app.post("/api/v1/seed-categorias")
def seed_categorias(db: Session = Depends(get_db)):
    """Insere categorias padrão no sistema"""
    categorias_padrao = [
        {"nome": "Motoboys", "descricao": "Pagamentos para entregadores", "cor": "#28a745"},
        {"nome": "Boletos", "descricao": "Contas e boletos diversos", "cor": "#dc3545"},
        {"nome": "Impostos", "descricao": "Impostos e taxas", "cor": "#6f42c1"},
        {"nome": "Aluguel", "descricao": "Aluguel do imóvel", "cor": "#fd7e14"},
        {"nome": "Produtos", "descricao": "Compra de ingredientes e produtos", "cor": "#20c997"},
        {"nome": "Contas Fixas", "descricao": "Contas mensais fixas", "cor": "#17a2b8"},
        {"nome": "Internet", "descricao": "Internet e telefone", "cor": "#6c757d"},
        {"nome": "Salários", "descricao": "Pagamento de funcionários", "cor": "#ffc107"}
    ]
    
    for cat_data in categorias_padrao:
        # Verificar se a categoria já existe
        existing = db.query(models.Categoria).filter(models.Categoria.nome == cat_data["nome"]).first()
        if not existing:
            categoria = models.Categoria(**cat_data)
            db.add(categoria)
    
    db.commit()
    return {"message": "Categorias padrão inseridas com sucesso"}
