from peewee import Model, CharField, FloatField, DateField, TextField, DateTimeField
from datetime import datetime
from .db import db

class BaseModel(Model):
    """Modelo base com configuração do banco"""
    class Meta:
        database = db

class Categoria(BaseModel):
    """Modelo para categorias de despesas"""
    nome = CharField(unique=True, max_length=50)
    descricao = TextField(null=True)
    cor = CharField(max_length=7, default="#007bff")  # Código de cor hex
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'categorias'
    
    def __str__(self):
        return self.nome

class Despesa(BaseModel):
    """Modelo para despesas da pizzaria"""
    descricao = CharField(max_length=200)
    categoria = CharField(max_length=50)  # Nome da categoria
    valor = FloatField()
    data_vencimento = DateField(null=True)
    data_pagamento = DateField(null=True)
    observacoes = TextField(null=True)
    status = CharField(max_length=20, default="pendente")  # pendente, pago, atrasado
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'despesas'
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor:.2f}"
    
    def save(self, *args, **kwargs):
        """Atualiza o campo updated_at ao salvar"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

