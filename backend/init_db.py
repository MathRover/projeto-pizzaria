#!/usr/bin/env python3
"""
Script para inicializar o banco de dados da pizzaria.
Execute este script após iniciar o servidor para criar as tabelas e inserir categorias padrão.
"""

import requests
import json
import time

# URL base da API
BASE_URL = "http://localhost:8000"

def aguardar_servidor():
    """Aguarda o servidor estar disponível"""
    print("🔄 Aguardando servidor estar disponível...")
    
    max_tentativas = 30
    tentativa = 0
    
    while tentativa < max_tentativas:
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✅ Servidor está rodando!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        tentativa += 1
        time.sleep(1)
        print(f"⏳ Tentativa {tentativa}/{max_tentativas}...")
    
    print("❌ Servidor não respondeu após 30 tentativas")
    return False

def inserir_categorias_padrao():
    """Insere categorias padrão no sistema"""
    print("🍕 Inserindo categorias padrão...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/seed-categorias")
        
        if response.status_code == 200:
            print("✅ Categorias padrão inseridas com sucesso!")
            return True
        else:
            print(f"❌ Erro ao inserir categorias: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def verificar_categorias():
    """Verifica se as categorias foram inseridas corretamente"""
    print("🔍 Verificando categorias inseridas...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/categorias")
        
        if response.status_code == 200:
            categorias = response.json()
            print(f"✅ {len(categorias)} categorias encontradas:")
            
            for cat in categorias:
                print(f"   • {cat['nome']} - {cat['descricao']}")
            
            return True
        else:
            print(f"❌ Erro ao verificar categorias: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar categorias: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Inicializando banco de dados da pizzaria...")
    print("=" * 50)
    
    # Aguardar servidor
    if not aguardar_servidor():
        return
    
    print()
    
    # Inserir categorias padrão
    if not inserir_categorias_padrao():
        return
    
    print()
    
    # Verificar categorias
    if not verificar_categorias():
        return
    
    print()
    print("🎉 Inicialização concluída com sucesso!")
    print("Acesse http://localhost:3000 para usar o sistema")

if __name__ == "__main__":
    main()
