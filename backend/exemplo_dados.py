#!/usr/bin/env python3
"""
Script para inserir dados de exemplo no sistema da pizzaria.
Execute este script após iniciar o servidor para ter dados para testar.
"""

import requests
import json
from datetime import date, timedelta

# URL base da API
BASE_URL = "http://localhost:8000/api/v1"

def inserir_dados_exemplo():
    """Insere dados de exemplo no sistema"""
    
    print("🍕 Inserindo dados de exemplo no sistema da pizzaria...")
    
    # Dados de exemplo
    despesas_exemplo = [
        {
            "descricao": "Pagamento motoboy João - Entrega zona sul",
            "categoria": "Motoboys",
            "valor": 25.00,
            "data_vencimento": str(date.today()),
            "status": "pago"
        },
        {
            "descricao": "Pagamento motoboy Maria - Entrega zona norte",
            "categoria": "Motoboys",
            "valor": 30.00,
            "data_vencimento": str(date.today()),
            "status": "pendente"
        },
        {
            "descricao": "Boleto energia elétrica - Janeiro 2024",
            "categoria": "Boletos",
            "valor": 450.00,
            "data_vencimento": str(date.today() + timedelta(days=5)),
            "status": "pendente"
        },
        {
            "descricao": "Boleto água - Janeiro 2024",
            "categoria": "Boletos",
            "valor": 120.00,
            "data_vencimento": str(date.today() + timedelta(days=3)),
            "status": "pendente"
        },
        {
            "descricao": "ICMS - Janeiro 2024",
            "categoria": "Impostos",
            "valor": 850.00,
            "data_vencimento": str(date.today() + timedelta(days=10)),
            "status": "pendente"
        },
        {
            "descricao": "Aluguel do imóvel - Janeiro 2024",
            "categoria": "Aluguel",
            "valor": 2500.00,
            "data_vencimento": str(date.today() + timedelta(days=2)),
            "status": "pendente"
        },
        {
            "descricao": "Compra de farinha de trigo - 50kg",
            "categoria": "Produtos",
            "valor": 180.00,
            "data_vencimento": str(date.today()),
            "status": "pago"
        },
        {
            "descricao": "Compra de queijo mussarela - 20kg",
            "categoria": "Produtos",
            "valor": 320.00,
            "data_vencimento": str(date.today()),
            "status": "pago"
        },
        {
            "descricao": "Compra de tomates - 30kg",
            "categoria": "Produtos",
            "valor": 90.00,
            "data_vencimento": str(date.today()),
            "status": "pago"
        },
        {
            "descricao": "Conta de gás - Janeiro 2024",
            "categoria": "Contas Fixas",
            "valor": 85.00,
            "data_vencimento": str(date.today() + timedelta(days=7)),
            "status": "pendente"
        },
        {
            "descricao": "Internet e telefone - Janeiro 2024",
            "categoria": "Internet",
            "valor": 150.00,
            "data_vencimento": str(date.today() + timedelta(days=15)),
            "status": "pendente"
        },
        {
            "descricao": "Salário funcionário Carlos - Cozinheiro",
            "categoria": "Salários",
            "valor": 1800.00,
            "data_vencimento": str(date.today() + timedelta(days=1)),
            "status": "pendente"
        },
        {
            "descricao": "Salário funcionária Ana - Atendente",
            "categoria": "Salários",
            "valor": 1500.00,
            "data_vencimento": str(date.today() + timedelta(days=1)),
            "status": "pendente"
        }
    ]
    
    # Inserir cada despesa
    for i, despesa in enumerate(despesas_exemplo, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/despesas",
                json=despesa,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                print(f"✅ Despesa {i}/{len(despesas_exemplo)} inserida: {despesa['descricao']}")
            else:
                print(f"❌ Erro ao inserir despesa {i}: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Erro: Não foi possível conectar ao servidor.")
            print("Certifique-se de que o servidor está rodando em http://localhost:8000")
            return
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    print("\n🎉 Dados de exemplo inseridos com sucesso!")
    print("Acesse http://localhost:3000 para ver o sistema funcionando.")

if __name__ == "__main__":
    inserir_dados_exemplo()


