# MercadoPro — Fase 5

## Entregue
- Caixa real no PostgreSQL: abertura, fechamento, saldo esperado e diferença.
- Sangria e suprimento.
- Pagamentos de venda: dinheiro, PIX, débito, crédito e múltiplos pagamentos.
- Cálculo de troco para dinheiro.
- Venda exige caixa aberto e pagamento suficiente.
- Pagamentos vinculados à venda.
- Movimentação de caixa vinculada à venda em dinheiro.
- Estorno de dinheiro ao cancelar venda.
- Dashboard passa a consultar o saldo do caixa aberto.
- Nova tela de Caixa.
- Modal de pagamento integrado ao PDV.
- Interface premium com linguagem visual inspirada em produtos de IA: gradientes, glass, microstatus, assistente operacional, scanner online e estados inteligentes.

## Tabelas
- `cash_registers`
- `cash_movements`
- `sale_payments`

## Endpoints
- `GET /api/cash/status`
- `POST /api/cash/open`
- `POST /api/cash/movement`
- `POST /api/cash/close`
- `GET /api/cash/history`
- `POST /api/sales/{id}/finalize`

## Regras importantes
- Abrir/fechar caixa e sangria/suprimento exigem ADMINISTRADOR ou GERENTE.
- Venda finalizada exige caixa aberto e pagamento suficiente.
- Troco somente é permitido em dinheiro.
- Cancelamento de venda paga em dinheiro exige caixa aberto para registrar o estorno.
- Fechamento calcula valor esperado a partir do saldo inicial e movimentos, sem duplicar o movimento de abertura.

## Visual
A Fase 5 também refina o visual do sistema para fugir de uma interface administrativa genérica. O PDV recebe uma linguagem visual de operação inteligente e o Caixa recebe cards, estados online/offline, gradientes e indicadores de operação.

## Testes
- Backend Python compilado com sucesso.
- Build completo do frontend depende da instalação local das dependências npm (`npm install`).
