import React, { useState, useEffect } from 'react';
import { Despesa, DespesaCreate, DespesaUpdate, Categoria } from '../types';
import './DespesaForm.css';

interface DespesaFormProps {
  despesa?: Despesa;
  onSubmit: (data: DespesaCreate | DespesaUpdate) => void;
  onCancel: () => void;
  isEditing?: boolean;
}

const DespesaForm: React.FC<DespesaFormProps> = ({
  despesa,
  onSubmit,
  onCancel,
  isEditing = false
}) => {
  const [formData, setFormData] = useState<DespesaCreate>({
    descricao: '',
    categoria: '',
    valor: 0,
    data_vencimento: '',
    data_pagamento: '',
    observacoes: '',
    status: 'pendente'
  });

  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(true);

  // Carregar categorias quando o componente montar
  useEffect(() => {
    fetchCategorias();
  }, []);

  // Preencher formulário se estiver editando
  useEffect(() => {
    if (despesa && isEditing) {
      setFormData({
        descricao: despesa.descricao,
        categoria: despesa.categoria,
        valor: despesa.valor,
        data_vencimento: despesa.data_vencimento || '',
        data_pagamento: despesa.data_pagamento || '',
        observacoes: despesa.observacoes || '',
        status: despesa.status
      });
    }
  }, [despesa, isEditing]);

  const fetchCategorias = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/categorias');
      if (response.ok) {
        const data = await response.json();
        setCategorias(data);
      } else {
        console.error('Erro ao carregar categorias:', response.statusText);
        // Se não conseguir carregar categorias, usar categorias padrão
        setCategorias([
          { id: 1, nome: 'Motoboys', descricao: 'Pagamentos para entregadores', cor: '#28a745' },
          { id: 2, nome: 'Boletos', descricao: 'Contas e boletos diversos', cor: '#dc3545' },
          { id: 3, nome: 'Impostos', descricao: 'Impostos e taxas', cor: '#6f42c1' },
          { id: 4, nome: 'Aluguel', descricao: 'Aluguel do imóvel', cor: '#fd7e14' },
          { id: 5, nome: 'Produtos', descricao: 'Compra de ingredientes e produtos', cor: '#20c997' },
          { id: 6, nome: 'Contas Fixas', descricao: 'Contas mensais fixas', cor: '#17a2b8' },
          { id: 7, nome: 'Internet', descricao: 'Internet e telefone', cor: '#6c757d' },
          { id: 8, nome: 'Salários', descricao: 'Pagamento de funcionários', cor: '#ffc107' }
        ]);
      }
    } catch (error) {
      console.error('Erro ao carregar categorias:', error);
      // Em caso de erro, usar categorias padrão
      setCategorias([
        { id: 1, nome: 'Motoboys', descricao: 'Pagamentos para entregadores', cor: '#28a745' },
        { id: 2, nome: 'Boletos', descricao: 'Contas e boletos diversos', cor: '#dc3545' },
        { id: 3, nome: 'Impostos', descricao: 'Impostos e taxas', cor: '#6f42c1' },
        { id: 4, nome: 'Aluguel', descricao: 'Aluguel do imóvel', cor: '#fd7e14' },
        { id: 5, nome: 'Produtos', descricao: 'Compra de ingredientes e produtos', cor: '#20c997' },
        { id: 6, nome: 'Contas Fixas', descricao: 'Contas mensais fixas', cor: '#17a2b8' },
        { id: 7, nome: 'Internet', descricao: 'Internet e telefone', cor: '#6c757d' },
        { id: 8, nome: 'Salários', descricao: 'Pagamento de funcionários', cor: '#ffc107' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'valor' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validação básica
    if (!formData.descricao.trim()) {
      alert('Por favor, preencha a descrição');
      return;
    }
    
    if (!formData.categoria) {
      alert('Por favor, selecione uma categoria');
      return;
    }
    
    if (formData.valor <= 0) {
      alert('Por favor, insira um valor válido');
      return;
    }

    onSubmit(formData);
  };

  if (loading) {
    return (
      <div className="despesa-form-container">
        <div className="loading-spinner"></div>
        <p>Carregando categorias...</p>
      </div>
    );
  }

  return (
    <div className="despesa-form-container">
      <h2>{isEditing ? 'Editar Despesa' : 'Nova Despesa'}</h2>
      
      <form onSubmit={handleSubmit} className="despesa-form">
        <div className="form-group">
          <label htmlFor="descricao">Descrição *</label>
          <input
            type="text"
            id="descricao"
            name="descricao"
            value={formData.descricao}
            onChange={handleChange}
            placeholder="Ex: Pagamento motoboy João"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="categoria">Categoria *</label>
          <select
            id="categoria"
            name="categoria"
            value={formData.categoria}
            onChange={handleChange}
            required
          >
            <option value="">Selecione uma categoria</option>
            {categorias.map(cat => (
              <option key={cat.id} value={cat.nome}>
                {cat.nome}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="valor">Valor (R$) *</label>
          <input
            type="number"
            id="valor"
            name="valor"
            value={formData.valor}
            onChange={handleChange}
            step="0.01"
            min="0"
            placeholder="0.00"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="data_vencimento">Data de Vencimento</label>
            <input
              type="date"
              id="data_vencimento"
              name="data_vencimento"
              value={formData.data_vencimento}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="data_pagamento">Data de Pagamento</label>
            <input
              type="date"
              id="data_pagamento"
              name="data_pagamento"
              value={formData.data_pagamento}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="status">Status</label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="pendente">Pendente</option>
            <option value="pago">Pago</option>
            <option value="atrasado">Atrasado</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="observacoes">Observações</label>
          <textarea
            id="observacoes"
            name="observacoes"
            value={formData.observacoes}
            onChange={handleChange}
            placeholder="Observações adicionais..."
            rows={3}
          />
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} className="btn btn-secondary">
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary">
            {isEditing ? 'Atualizar' : 'Salvar'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default DespesaForm;


