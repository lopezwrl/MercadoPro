# MercadoPro — Fase 2

## Implementado
- Produtos: CRUD, pesquisa, paginação, filtros, preço, margem e status.
- Categorias, marcas e unidades de medida.
- Subcategorias vinculadas a categorias.
- Estoque atual, mínimo e máximo.
- Movimentações ENTRY, EXIT, ADJUSTMENT, LOSS e RETURN.
- Histórico de movimentações.
- Validação de código interno e código de barras únicos.
- Valores monetários com Decimal/Numeric.
- Auditoria de produtos e movimentações.
- Dashboard com indicadores reais de produtos/estoque.
- Seed inicial para categorias, marcas e unidades.

## Parcial
- Leitor de código de barras: API e campos estão preparados; integração física do leitor será usada naturalmente como entrada de teclado.
- Validade: campo e indicador foram preparados, mas regras avançadas ficam para etapa posterior.
- Permissões: reaproveita autenticação da Fase 1 e restringe alterações de estoque/cadastro aos perfis ADMINISTRADOR, GERENTE e ESTOQUE.

## Ainda não implementado
- PDV, vendas, fornecedores/pedidos de compra, financeiro e relatórios completos (fases futuras).
- Migrations formais; nesta versão a estrutura é criada pelo SQLAlchemy `create_all` no startup.

## Próximo passo
Testar o ambiente local, cadastrar produtos e validar as movimentações antes de iniciar a Fase 3.
