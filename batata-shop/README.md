# Batata Prime (com banco de dados)

Site funcional de venda de batatas com frontend moderno + backend Python + banco SQLite.

## Requisitos
- Python 3.10+

## Como rodar
```bash
python3 server.py
```

Acesse: http://localhost:4173

## O que está funcionando
- Cardápio carregado do banco SQLite (`products`)
- Carrinho no frontend (adicionar/remover itens)
- Finalização de pedido com nome e WhatsApp
- Pedido salvo no banco (`orders` e `order_items`)

## API
- `GET /api/health`
- `GET /api/products`
- `POST /api/orders`
- `GET /api/orders/:orderId`
