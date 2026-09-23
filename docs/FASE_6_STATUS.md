# MercadoPro — Fase 6 Status

## Objetivo
Implementar o núcleo financeiro: contas a pagar, contas a receber, categorias, lançamentos, baixas, cancelamentos e visão de fluxo/projeção.

## Concluído
- Tabelas `financial_categories` e `financial_entries`.
- API `/api/finance/summary`.
- API de categorias.
- API de lançamentos.
- Baixa de lançamento.
- Cancelamento de lançamento pendente.
- Resumo de vendas e compras do mês.
- Indicadores de contas a pagar/receber e vencidos.
- Projeção operacional.
- Tela Financeiro com visão geral, contas a pagar, contas a receber e novo lançamento.
- Nova identidade visual do Financeiro inspirada em padrões atuais de SaaS/AI: cards modulares, hierarquia bento, camadas, glow discreto, estados e modo escuro.

## Parcial / preparado
- Integração financeira com compras e vendas via indicadores e estrutura. Regras de parcelamento, vencimentos derivados de condição de pagamento e conciliação bancária ficam para uma evolução posterior.
- O caixa da Fase 5 continua separado do módulo de lançamentos financeiros para evitar dupla contabilização automática sem uma regra de competência definida.

## Testes
- Backend: `python -m compileall -q app` — OK.
- Frontend: a instalação/build do npm não foi concluída no ambiente de geração dentro do tempo disponível; executar `npm install` e `npm run build` localmente.

## Próximo passo
Fase 7 — Relatórios, filtros avançados, exportações e análises gerenciais.
