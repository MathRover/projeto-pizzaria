from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Despesa(Base):
    """Modelo para representar uma despesa da pizzaria"""
    __tablename__ = "despesas"
    
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(200), nullable=False, index=True)
    categoria = Column(String(50), nullable=False, index=True)
    valor = Column(Float, nullable=False)
    data_vencimento = Column(Date, nullable=True)
    data_pagamento = Column(Date, nullable=True)
    observacoes = Column(Text, nullable=True)
    status = Column(String(20), default="pendente")  # pendente, pago, atrasado
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    def __repr__(self):
        return f"<Despesa(id={self.id}, descricao='{self.descricao}', valor={self.valor})>"

class Categoria(Base):
    """Modelo para categorias de despesas"""
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    cor = Column(String(7), default="#007bff")  # Código de cor hex
    
    def __repr__(self):
        return f"<Categoria(id={self.id}, nome='{self.nome}')>"

