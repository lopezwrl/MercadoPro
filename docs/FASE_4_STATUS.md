# MercadoPro — Fase 4 — Status

## Concluído
- Cadastro de clientes com CPF/CNPJ opcionais, contatos, endereço, ativação/inativação e pesquisa.
- Estrutura PostgreSQL `customers`, `sales` e `sale_items`.
- PDV com carrinho, código interno/código de barras, cliente, quantidade, desconto e total.
- Atalhos F2/F3/F4/F5/F6/F7 e ESC preservado para operação/navegação do navegador.
- Finalização transacional: venda + itens + baixa de estoque + movimentação EXIT + auditoria.
- Validação de estoque para impedir estoque negativo.
- Histórico e detalhe de vendas.
- Cancelamento de venda finalizada com devolução de estoque e movimentação RETURN.
- Cancelamento restrito a ADMINISTRADOR e GERENTE.
- Dashboard passou a consultar vendas reais do PostgreSQL.
- Seed de três clientes de demonstração sem documentos reais.

## Parcial / pendente
- Pagamentos completos, troco, múltiplos pagamentos e fechamento de caixa ficam para a Fase 5.
- Limites comerciais de desconto por papel ainda não possuem política configurada; o campo existe no PDV e na venda.
- Validação matemática de CPF/CNPJ não foi criada para não inventar regra fiscal/comercial.
- Build do frontend não foi executado neste ambiente porque as dependências npm não puderam ser instaladas dentro do tempo disponível; backend foi validado com `compileall`.

## Arquivos principais
- `backend/app/models/models.py`
- `backend/app/routers/sales.py`
- `backend/app/routers/dashboard.py`
- `backend/app/main.py`
- `frontend/src/App.jsx`
- `frontend/src/services/api.js`
- `frontend/src/styles.css`

## Endpoints
- `GET/POST /api/customers`
- `PATCH /api/customers/{id}`
- `PATCH /api/customers/{id}/status`
- `GET /api/sales`
- `GET /api/sales/search`
- `GET /api/sales/{id}`
- `POST /api/sales`
- `POST /api/sales/{id}/items`
- `POST /api/sales/{id}/finalize`
- `POST /api/sales/{id}/cancel`

## Próximo passo
Fase 5: caixa, formas de pagamento, valor recebido, troco, múltiplos pagamentos e fechamento.
