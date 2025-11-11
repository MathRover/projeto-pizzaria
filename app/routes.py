"""
Rotas da aplicação Flask
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from peewee import fn
from database.models import Despesa, Categoria
from database.db import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal com lista de despesas"""
    # Obter filtros
    categoria_filtro = request.args.get('categoria', '')
    status_filtro = request.args.get('status', '')
    busca = request.args.get('busca', '')
    data_busca = request.args.get('data_busca', '')
    
    # Construir query
    query = Despesa.select().order_by(Despesa.created_at.desc())
    
    if categoria_filtro:
        query = query.where(Despesa.categoria == categoria_filtro)
    
    if status_filtro:
        query = query.where(Despesa.status == status_filtro)
    
    if busca:
        query = query.where(Despesa.descricao.contains(busca))
    
    # Filtro por data (busca em vencimento, pagamento ou criação)
    if data_busca:
        try:
            data_b = datetime.strptime(data_busca, '%Y-%m-%d').date()
            query = query.where(
                (Despesa.data_vencimento == data_b) |
                (Despesa.data_pagamento == data_b) |
                (fn.date(Despesa.created_at) == data_b)
            )
        except:
            pass
    
    despesas = list(query)
    
    # Obter categorias para filtro
    categorias = list(Categoria.select())
    
    # Calcular estatísticas
    total_despesas = Despesa.select().count()
    total_valor = sum(d.valor for d in Despesa.select())
    despesas_pendentes = Despesa.select().where(Despesa.status == 'pendente').count()
    despesas_pagas = Despesa.select().where(Despesa.status == 'pago').count()
    
    estatisticas = {
        'total_despesas': total_despesas,
        'total_valor': total_valor,
        'despesas_pendentes': despesas_pendentes,
        'despesas_pagas': despesas_pagas
    }
    
    return render_template('index.html', 
                         despesas=despesas, 
                         categorias=categorias,
                         estatisticas=estatisticas,
                         categoria_filtro=categoria_filtro,
                         status_filtro=status_filtro,
                         busca=busca,
                         data_busca=data_busca)

@main_bp.route('/despesa/nova', methods=['GET', 'POST'])
def nova_despesa():
    """Criar nova despesa"""
    if request.method == 'POST':
        try:
            # Converter datas
            data_vencimento = None
            data_pagamento = None
            
            if request.form.get('data_vencimento'):
                data_vencimento = datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d').date()
            
            if request.form.get('data_pagamento'):
                data_pagamento = datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d').date()
            
            Despesa.create(
                descricao=request.form['descricao'],
                categoria=request.form['categoria'],
                valor=float(request.form['valor']),
                data_vencimento=data_vencimento,
                data_pagamento=data_pagamento,
                observacoes=request.form.get('observacoes', ''),
                status=request.form.get('status', 'pendente')
            )
            
            flash('Despesa criada com sucesso!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Erro ao criar despesa: {str(e)}', 'error')
    
    categorias = list(Categoria.select())
    return render_template('despesa_form.html', despesa=None, categorias=categorias)

@main_bp.route('/despesa/<int:despesa_id>/editar', methods=['GET', 'POST'])
def editar_despesa(despesa_id):
    """Editar despesa existente"""
    despesa = Despesa.get_or_none(Despesa.id == despesa_id)
    
    if not despesa:
        flash('Despesa não encontrada!', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            # Converter datas
            data_vencimento = None
            data_pagamento = None
            
            if request.form.get('data_vencimento'):
                data_vencimento = datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d').date()
            
            if request.form.get('data_pagamento'):
                data_pagamento = datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d').date()
            
            despesa.descricao = request.form['descricao']
            despesa.categoria = request.form['categoria']
            despesa.valor = float(request.form['valor'])
            despesa.data_vencimento = data_vencimento
            despesa.data_pagamento = data_pagamento
            despesa.observacoes = request.form.get('observacoes', '')
            despesa.status = request.form.get('status', 'pendente')
            despesa.save()
            
            flash('Despesa atualizada com sucesso!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Erro ao atualizar despesa: {str(e)}', 'error')
    
    categorias = list(Categoria.select())
    return render_template('despesa_form.html', despesa=despesa, categorias=categorias)

@main_bp.route('/despesa/<int:despesa_id>/excluir', methods=['POST'])
def excluir_despesa(despesa_id):
    """Excluir despesa"""
    despesa = Despesa.get_or_none(Despesa.id == despesa_id)
    
    if not despesa:
        flash('Despesa não encontrada!', 'error')
        return redirect(url_for('main.index'))
    
    try:
        despesa.delete_instance()
        flash('Despesa excluída com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir despesa: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

@main_bp.route('/despesa/<int:despesa_id>/status', methods=['POST'])
def alterar_status(despesa_id):
    """Alterar status da despesa"""
    despesa = Despesa.get_or_none(Despesa.id == despesa_id)
    
    if not despesa:
        return jsonify({'success': False, 'message': 'Despesa não encontrada'}), 404
    
    novo_status = request.json.get('status')
    if novo_status not in ['pendente', 'pago', 'atrasado']:
        return jsonify({'success': False, 'message': 'Status inválido'}), 400
    
    try:
        despesa.status = novo_status
        if novo_status == 'pago' and not despesa.data_pagamento:
            despesa.data_pagamento = date.today()
        despesa.save()
        return jsonify({'success': True, 'message': 'Status atualizado com sucesso'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main_bp.route('/api/estatisticas')
def api_estatisticas():
    """API para obter estatísticas"""
    total_despesas = Despesa.select().count()
    total_valor = sum(d.valor for d in Despesa.select())
    despesas_pendentes = Despesa.select().where(Despesa.status == 'pendente').count()
    despesas_pagas = Despesa.select().where(Despesa.status == 'pago').count()
    
    return jsonify({
        'total_despesas': total_despesas,
        'total_valor': float(total_valor),
        'despesas_pendentes': despesas_pendentes,
        'despesas_pagas': despesas_pagas
    })

