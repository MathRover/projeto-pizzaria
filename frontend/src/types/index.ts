// Tipos para as despesas da pizzaria
export interface Despesa {
  id: number;
  descricao: string;
  categoria: string;
  valor: number;
  data_vencimento?: string;
  data_pagamento?: string;
  observacoes?: string;
  status: 'pendente' | 'pago' | 'atrasado';
  created_at: string;
  updated_at?: string;
}

// Tipo para criar uma nova despesa
export interface DespesaCreate {
  descricao: string;
  categoria: string;
  valor: number;
  data_vencimento?: string;
  data_pagamento?: string;
  observacoes?: string;
  status?: string;
}

// Tipo para atualizar uma despesa
export interface DespesaUpdate {
  descricao?: string;
  categoria?: string;
  valor?: number;
  data_vencimento?: string;
  data_pagamento?: string;
  observacoes?: string;
  status?: string;
}

// Tipo para categoria
export interface Categoria {
  id: number;
  nome: string;
  descricao?: string;
  cor: string;
}

// Tipo para estatísticas
export interface Estatisticas {
  total_despesas: number;
  total_valor: number;
  despesas_pendentes: number;
  despesas_pagas: number;
}

// Tipo para filtros
export interface FiltrosDespesa {
  categoria?: string;
  status?: string;
  data_inicio?: string;
  data_fim?: string;
}


