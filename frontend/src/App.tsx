import React, { useState, useEffect } from 'react';
import DespesaForm from './components/DespesaForm';
import DespesaList from './components/DespesaList';
import { Despesa, DespesaCreate, DespesaUpdate, Estatisticas } from './types';
import './App.css';

const App: React.FC = () => {
  const [despesas, setDespesas] = useState<Despesa[]>([]);
  const [estatisticas, setEstatisticas] = useState<Estatisticas>({
    total_despesas: 0,
    total_valor: 0,
    despesas_pendentes: 0,
    despesas_pagas: 0
  });
  const [showForm, setShowForm] = useState(false);
  const [editingDespesa, setEditingDespesa] = useState<Despesa | null>(null);
  const [loading, setLoading] = useState(true);

  // Carregar despesas e estatísticas quando o componente montar
  useEffect(() => {
    fetchDespesas();
    fetchEstatisticas();
  }, []);

  const fetchDespesas = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/despesas');
      if (response.ok) {
        const data = await response.json();
        setDespesas(data);
      } else {
        console.error('Erro ao carregar despesas:', response.statusText);
      }
    } catch (error) {
      console.error('Erro ao carregar despesas:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEstatisticas = async () => {
    try {
      const response = await fetch('/api/v1/estatisticas');
      if (response.ok) {
        const data = await response.json();
        setEstatisticas(data);
      }
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleCreateDespesa = async (despesaData: DespesaCreate) => {
    try {
      const response = await fetch('/api/v1/despesas', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(despesaData),
      });

      if (response.ok) {
        const novaDespesa = await response.json();
        setDespesas(prev => [...prev, novaDespesa]);
        fetchEstatisticas();
        setShowForm(false);
        alert('Despesa criada com sucesso!');
      } else {
        alert('Erro ao criar despesa');
      }
    } catch (error) {
      console.error('Erro ao criar despesa:', error);
      alert('Erro ao criar despesa');
    }
  };

  const handleUpdateDespesa = async (despesaData: DespesaUpdate) => {
    if (!editingDespesa) return;

    try {
      const response = await fetch(`/api/v1/despesas/${editingDespesa.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(despesaData),
      });

      if (response.ok) {
        const despesaAtualizada = await response.json();
        setDespesas(prev => 
          prev.map(d => d.id === editingDespesa.id ? despesaAtualizada : d)
        );
        fetchEstatisticas();
        setEditingDespesa(null);
        alert('Despesa atualizada com sucesso!');
      } else {
        alert('Erro ao atualizar despesa');
      }
    } catch (error) {
      console.error('Erro ao atualizar despesa:', error);
      alert('Erro ao atualizar despesa');
    }
  };

  const handleDeleteDespesa = async (id: number) => {
    try {
      const response = await fetch(`/api/v1/despesas/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setDespesas(prev => prev.filter(d => d.id !== id));
        fetchEstatisticas();
        alert('Despesa excluída com sucesso!');
      } else {
        alert('Erro ao excluir despesa');
      }
    } catch (error) {
      console.error('Erro ao excluir despesa:', error);
      alert('Erro ao excluir despesa');
    }
  };

  const handleStatusChange = async (id: number, status: string) => {
    try {
      const response = await fetch(`/api/v1/despesas/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });

      if (response.ok) {
        const despesaAtualizada = await response.json();
        setDespesas(prev => 
          prev.map(d => d.id === id ? despesaAtualizada : d)
        );
        fetchEstatisticas();
      }
    } catch (error) {
      console.error('Erro ao alterar status:', error);
    }
  };

  const handleEdit = (despesa: Despesa) => {
    setEditingDespesa(despesa);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingDespesa(null);
  };

  const handleSubmitForm = (data: DespesaCreate | DespesaUpdate) => {
    if (editingDespesa) {
      handleUpdateDespesa(data);
    } else {
      handleCreateDespesa(data as DespesaCreate);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Carregando sistema...</p>
      </div>
    );
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🍕 Sistema de Fechamento de Caixa</h1>
          <p>Gerencie todas as despesas da sua pizzaria</p>
        </div>
      </header>

      {/* Estatísticas principais */}
      <div className="estatisticas-principais">
        <div className="stat-card principal">
          <span className="stat-label">Total de Despesas</span>
          <span className="stat-value">{estatisticas.total_despesas}</span>
        </div>
        <div className="stat-card principal">
          <span className="stat-label">Valor Total</span>
          <span className="stat-value">
            {new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL'
            }).format(estatisticas.total_valor)}
          </span>
        </div>
        <div className="stat-card principal">
          <span className="stat-label">Pendentes</span>
          <span className="stat-value">{estatisticas.despesas_pendentes}</span>
        </div>
        <div className="stat-card principal">
          <span className="stat-label">Pagas</span>
          <span className="stat-value">{estatisticas.despesas_pagas}</span>
        </div>
      </div>

      {/* Conteúdo principal */}
      <main className="app-main">
        {/* Botão para adicionar nova despesa */}
        <div className="actions-bar">
          <button
            onClick={() => setShowForm(true)}
            className="btn btn-primary btn-large"
            disabled={showForm}
          >
            ➕ Nova Despesa
          </button>
        </div>

        {/* Formulário ou lista */}
        {showForm ? (
          <DespesaForm
            despesa={editingDespesa || undefined}
            onSubmit={handleSubmitForm}
            onCancel={handleCancelForm}
            isEditing={!!editingDespesa}
          />
        ) : (
          <DespesaList
            despesas={despesas}
            onEdit={handleEdit}
            onDelete={handleDeleteDespesa}
            onStatusChange={handleStatusChange}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>&copy; 2024 Sistema Pizzaria - Desenvolvido para controle de despesas</p>
      </footer>
    </div>
  );
};

export default App;


