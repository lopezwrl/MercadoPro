# MercadoPro — Fase 3 — Status

## Implementado
- Modelos PostgreSQL para fornecedores, relação fornecedor/produto, compras e itens.
- APIs de fornecedores e compras.
- Compras em rascunho, finalização e cancelamento.
- Entrada de estoque transacional ao finalizar compra.
- Estorno de estoque ao cancelar compra finalizada.
- Custo médio ponderado do produto na entrada, sem alterar automaticamente o preço de venda.
- Auditoria das operações principais.
- Seeds de três fornecedores de demonstração.
- Frontend com telas de Fornecedores e Compras.
- Inclusão de fornecedores e compras no menu existente.

## Parcial / limitações
- O leitor de código de barras está preparado pela seleção de produto, mas a UX dedicada de captura física pode ser refinada na Fase 4/5.
- A tela de detalhes de compra ainda usa uma visualização simples; pode receber uma página/modal detalhado em refinamento posterior.
- Integração financeira fica somente preparada, conforme o escopo.

## Importante
A criação automática de tabelas usa `Base.metadata.create_all`, como na Fase 1/2. Como as tabelas novas são adicionadas, elas são criadas sem apagar as existentes.

## Não implementado nesta fase
- Contas a pagar completas.
- PDV/vendas.
- Fiscal.
- Integrações com equipamentos.

## Testes recomendados
1. Criar fornecedor.
2. Criar rascunho de compra.
3. Finalizar compra.
4. Conferir estoque e histórico de movimentação.
5. Cancelar compra finalizada.
6. Conferir estorno.
7. Conferir dashboard.

## Próximo passo
Fase 4 — Clientes + PDV + carrinho + vendas, somente após validar esta fase.
