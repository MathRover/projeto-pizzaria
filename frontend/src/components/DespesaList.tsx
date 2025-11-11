import React, { useState, useEffect } from 'react';
import { Despesa, Categoria } from '../types';
import './DespesaList.css';

interface DespesaListProps {
  despesas: Despesa[];
  onEdit: (despesa: Despesa) => void;
  onDelete: (id: number) => void;
  onStatusChange: (id: number, status: string) => void;
}

const DespesaList: React.FC<DespesaListProps> = ({
  despesas,
  onEdit,
  onDelete,
  onStatusChange
}) => {
  const [filteredDespesas, setFilteredDespesas] = useState<Despesa[]>(despesas);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategoria, setFilterCategoria] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [categorias, setCategorias] = useState<Categoria[]>([]);

  // Carregar categorias para exibição
  useEffect(() => {
    fetchCategorias();
  }, []);

  // Atualizar lista filtrada quando despesas mudarem
  useEffect(() => {
    let filtered = despesas;

    if (searchTerm) {
      filtered = filtered.filter(despesa =>
        despesa.descricao.toLowerCase().includes(searchTerm.toLowerCase()) ||
        despesa.categoria.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterCategoria) {
      filtered = filtered.filter(despesa => despesa.categoria === filterCategoria);
    }

    if (filterStatus) {
      filtered = filtered.filter(despesa => despesa.status === filterStatus);
    }

    setFilteredDespesas(filtered);
  }, [despesas, searchTerm, filterCategoria, filterStatus]);

  const fetchCategorias = async () => {
    try {
      const response = await fetch('/api/v1/categorias');
      if (response.ok) {
        const data = await response.json();
        setCategorias(data);
      } else {
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
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pago': return '#28a745';
      case 'pendente': return '#ffc107';
      case 'atrasado': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const getCategoriaColor = (categoriaNome: string) => {
    const categoria = categorias.find(cat => cat.nome === categoriaNome);
    return categoria ? categoria.cor : '#007bff';
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta despesa?')) {
      onDelete(id);
    }
  };

  const getCategoriasUnicas = () => {
    const categorias = [...new Set(despesas.map(d => d.categoria))];
    return categorias.sort();
  };

  return (
    <div className="despesa-list-container">
      <div className="filtros">
        <div className="filtro-grupo">
          <input
            type="text"
            placeholder="Buscar por descrição ou categoria..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="filtro-input"
          />
        </div>

        <div className="filtro-grupo">
          <select
            value={filterCategoria}
            onChange={(e) => setFilterCategoria(e.target.value)}
            className="filtro-select"
          >
            <option value="">Todas as categorias</option>
            {getCategoriasUnicas().map(categoria => (
              <option key={categoria} value={categoria}>{categoria}</option>
            ))}
          </select>
        </div>

        <div className="filtro-grupo">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filtro-select"
          >
            <option value="">Todos os status</option>
            <option value="pendente">Pendente</option>
            <option value="pago">Pago</option>
            <option value="atrasado">Atrasado</option>
          </select>
        </div>
      </div>

      <div className="estatisticas-rapidas">
        <div className="stat-card">
          <span className="stat-label">Total de Despesas</span>
          <span className="stat-value">{filteredDespesas.length}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Valor Total</span>
          <span className="stat-value">
            {formatCurrency(filteredDespesas.reduce((sum, d) => sum + d.valor, 0))}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Pendentes</span>
          <span className="stat-value">
            {filteredDespesas.filter(d => d.status === 'pendente').length}
          </span>
        </div>
      </div>

      <div className="table-container">
        <table className="despesa-table">
          <thead>
            <tr>
              <th>Descrição</th>
              <th>Categoria</th>
              <th>Valor</th>
              <th>Vencimento</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {filteredDespesas.length === 0 ? (
              <tr>
                <td colSpan={6} className="no-data">Nenhuma despesa encontrada</td>
              </tr>
            ) : (
              filteredDespesas.map(despesa => (
                <tr key={despesa.id}>
                  <td>
                    <div className="descricao-cell">
                      <strong>{despesa.descricao}</strong>
                      {despesa.observacoes && (
                        <small className="observacoes">{despesa.observacoes}</small>
                      )}
                    </div>
                  </td>
                  <td>
                    <span
                      className="categoria-tag"
                      style={{ backgroundColor: getCategoriaColor(despesa.categoria) }}
                    >
                      {despesa.categoria}
                    </span>
                  </td>
                  <td>
                    <strong className="valor">{formatCurrency(despesa.valor)}</strong>
                  </td>
                  <td>{formatDate(despesa.data_vencimento ?? '')}</td>
                  <td>
                    <select
                      value={despesa.status}
                      onChange={(e) => onStatusChange(despesa.id, e.target.value)}
                      className="status-select"
                      style={{ borderColor: getStatusColor(despesa.status) }}
                    >
                      <option value="pendente">Pendente</option>
                      <option value="pago">Pago</option>
                      <option value="atrasado">Atrasado</option>
                    </select>
                  </td>
                  <td>
                    <div className="acoes">
                      <button
                        onClick={() => onEdit(despesa)}
                        className="btn-acao btn-editar"
                        title="Editar"
                      >
                        ✏️
                      </button>
                      <button
                        onClick={() => handleDelete(despesa.id)}
                        className="btn-acao btn-excluir"
                        title="Excluir"
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DespesaList;
