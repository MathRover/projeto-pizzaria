# 🍕 Sistema de Fechamento de Caixa - Pizzaria

Sistema completo para gerenciamento de despesas e controle financeiro de pizzarias, desenvolvido com **Flask**, **Jinja2**, **Peewee**, **HTML** e **CSS**.

## ✨ Funcionalidades

- ✅ **Gestão de Despesas**: Adicionar, editar, excluir e categorizar despesas
- ✅ **Categorias Inteligentes**: Sistema de categorização com cores e descrições
- ✅ **Controle de Status**: Pendente, Pago, Atrasado
- ✅ **Filtros Avançados**: Busca por descrição, categoria e status
- ✅ **Estatísticas em Tempo Real**: Total de despesas, valores e contadores
- ✅ **Interface Moderna**: Design responsivo e visual atraente
- ✅ **Simples e Rápido**: Tecnologias leves e eficientes

## 🚀 Início Rápido

### Windows
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
venv\Scripts\activate

# 3. Instalar dependências (instale cada uma separadamente)
pip install Flask==3.0.0
pip install peewee==3.17.0
pip install python-dotenv==1.0.0

# Ou instale tudo de uma vez:
pip install Flask==3.0.0 peewee==3.17.0 python-dotenv==1.0.0

# 4. Executar aplicação
python run.py
```

### Linux/Mac
```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Instalar dependências (instale cada uma separadamente)
pip install Flask==3.0.0
pip install peewee==3.17.0
pip install python-dotenv==1.0.0

# Ou instale tudo de uma vez:
pip install Flask==3.0.0 peewee==3.17.0 python-dotenv==1.0.0

# 4. Executar aplicação
python run.py
```

## 🌐 Acessar o Sistema

Após iniciar a aplicação, acesse:
- **Aplicação**: http://localhost:5000
- O banco de dados será criado automaticamente na primeira execução
- As categorias padrão serão inseridas automaticamente

## 🏗️ Arquitetura

### Estrutura do Projeto
```
projeto-pizzaria/
├── app/                    # Aplicação Flask
│   ├── __init__.py        # Factory da aplicação
│   └── routes.py          # Rotas e lógica de negócio
├── database/               # Configuração do banco (Peewee)
│   ├── __init__.py
│   ├── db.py              # Configuração e inicialização
│   └── models.py          # Modelos de dados
├── templates/             # Templates Jinja2 (HTML)
│   ├── base.html          # Template base
│   ├── index.html         # Lista de despesas
│   └── despesa_form.html  # Formulário de despesa
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos modernos
│   └── js/
│       └── main.js       # JavaScript
├── config.py             # Configurações
├── run.py                # Arquivo principal
└── requirements.txt      # Dependências
```

### Tecnologias Utilizadas

- **Flask 3.0.0** - Framework web leve e flexível
- **Jinja2** - Motor de templates (incluído no Flask)
- **Peewee 3.17.0** - ORM simples e intuitivo
- **SQLite** - Banco de dados embutido
- **HTML5** - Estrutura semântica
- **CSS3** - Estilização moderna com gradientes e animações

## 📊 Categorias Padrão

O sistema inclui automaticamente as seguintes categorias:

| Categoria | Cor | Descrição |
|-----------|-----|-----------|
| 🚚 Motoboys | 🟢 | Pagamentos para entregadores |
| 📄 Boletos | 🔴 | Contas e boletos diversos |
| 💰 Impostos | 🟣 | Impostos e taxas |
| 🏠 Aluguel | 🟠 | Aluguel do imóvel |
| 🥘 Produtos | 🟢 | Compra de ingredientes |
| 💡 Contas Fixas | 🔵 | Contas mensais fixas |
| 🌐 Internet | ⚫ | Internet e telefone |
| 👷 Salários | 🟡 | Pagamento de funcionários |

## 🎯 Como Usar

### 1. Criar Nova Despesa
- Clique em "Nova Despesa" no menu ou na página principal
- Preencha descrição, categoria, valor
- Adicione datas de vencimento/pagamento (opcional)
- Adicione observações (opcional)
- Selecione o status
- Clique em "Criar Despesa"

### 2. Gerenciar Despesas
- Visualize todas as despesas na tabela principal
- Use os filtros para buscar por descrição, categoria ou status
- Altere o status diretamente na tabela usando o dropdown
- Clique em ✏️ para editar uma despesa
- Clique em 🗑️ para excluir uma despesa

### 3. Acompanhar Estatísticas
- Veja o total de despesas no topo da página
- Acompanhe o valor total
- Monitore quantas estão pendentes e pagas

## 🔧 Configuração

### Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DATABASE=database/pizzaria.db
```

### Personalizar Categorias

As categorias padrão são inseridas automaticamente. Para adicionar novas categorias, você pode:

1. Editar o arquivo `database/db.py` na função `seed_categorias()`
2. Ou adicionar manualmente via código Python

## 🐛 Solução de Problemas

### Erro ao instalar dependências
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar novamente
pip install -r requirements.txt
```

### Porta 5000 já está em uso
Edite o arquivo `run.py` e altere a porta:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use outra porta
```

### Banco de dados não cria
- Verifique se a pasta `database/` existe
- Verifique permissões de escrita
- Execute manualmente: `python -c "from database.db import init_db; init_db()"`

### Categorias não aparecem
As categorias são inseridas automaticamente na primeira execução. Se não aparecerem:
```bash
python -c "from database.db import init_db; init_db(); from database.db import seed_categorias; seed_categorias()"
```

## 📝 Desenvolvimento

### Estrutura de Pastas Organizada

- **`app/`**: Lógica da aplicação Flask
- **`database/`**: Tudo relacionado ao banco de dados (Peewee)
- **`templates/`**: Templates HTML com Jinja2
- **`static/`**: CSS, JavaScript e outros arquivos estáticos

### Adicionar Novas Funcionalidades

1. **Nova Rota**: Adicione em `app/routes.py`
2. **Novo Modelo**: Adicione em `database/models.py`
3. **Novo Template**: Crie em `templates/` e use `base.html` como base
4. **Novo Estilo**: Adicione em `static/css/style.css`

## 🔮 Próximas Funcionalidades

- [ ] **Relatórios e gráficos**
- [ ] **Exportação para PDF/Excel**
- [ ] **Notificações de vencimento**
- [ ] **Backup automático do banco**
- [ ] **Múltiplas pizzarias**
- [ ] **Sistema de usuários**

## 📝 Licença

Este projeto foi desenvolvido por Matheus Rover

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---
