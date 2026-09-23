# MercadoPro — Fase 9

## Objetivo
Preparar o MercadoPro para integrações fiscais e equipamentos do ponto de venda, mantendo a regra de não simular uma autorização fiscal real.

## Implementado de verdade
- Nova central **Integrações** no frontend.
- Nova tabela PostgreSQL `integracoes`.
- Nova tabela PostgreSQL `equipamentos`.
- API `/api/integrations/overview`.
- API para salvar configurações de integração fiscal/impressão/scanner/balança.
- Cadastro e edição de equipamentos.
- Registro de teste de equipamento com data/hora e status.
- Auditoria das alterações de integrações e equipamentos.
- Proteção: somente `ADMINISTRADOR` altera integrações.
- Campos genéricos de segredo/senha não são persistidos pela API.
- Preparação fiscal com documento, UF, série e ambiente de homologação/produção.
- Interface preparada para impressão pelo navegador e leitura de scanner como teclado.

## O que NÃO foi falsamente considerado pronto
A emissão fiscal autorizada pela SEFAZ não foi simulada. Para produção ainda são necessários certificado digital, credenciais, parâmetros fiscais, regras tributárias por operação/UF e um conector/provedor homologado.

Também não foi prometida comunicação física universal com impressora, gaveta ou balança: o sistema registra a configuração e o teste local, mas o driver/protocolo efetivo depende do equipamento e do computador do caixa.

## Validação
- Backend: `python -m compileall` passou (`BACKEND_OK`).
- Frontend: `npm run build` não foi executado com sucesso neste ambiente porque o executável/dependências do Vite não estavam disponíveis. Não considerar o build validado até rodar localmente.

## Próximo passo
Depois da Fase 9, o núcleo funcional do escopo original está implementado. A próxima etapa deve ser **hardening e preparação para produção**, com testes integrados, permissões aplicadas a todas as rotas, observabilidade, migrações Alembic, backup agendado e escolha do provedor fiscal/equipamentos específico do mercado.
