from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
import os
import sqlite3
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.sqlite')
HOST = '0.0.0.0'
PORT = 4173


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(
        '''
        CREATE TABLE IF NOT EXISTS products (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          description TEXT NOT NULL,
          price REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          customer_name TEXT NOT NULL,
          customer_phone TEXT NOT NULL,
          total REAL NOT NULL,
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS order_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          order_id INTEGER NOT NULL,
          product_id INTEGER NOT NULL,
          product_name TEXT NOT NULL,
          quantity INTEGER NOT NULL,
          unit_price REAL NOT NULL,
          subtotal REAL NOT NULL,
          FOREIGN KEY(order_id) REFERENCES orders(id)
        );
        '''
    )

    count = cursor.execute('SELECT COUNT(*) AS count FROM products').fetchone()['count']

    if count == 0:
        cursor.executemany(
            'INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
            [
                ('Batata Cheddar & Bacon', 'Batata crocante, cheddar cremoso e bacon artesanal.', 29.9),
                ('Batata Supreme Frango', 'Frango desfiado, catupiry e ervas finas.', 32.5),
                ('Batata Veggie Especial', 'Legumes grelhados, molho verde e queijo vegano.', 27.0),
                ('Batata Picante Mexicana', 'Carne temperada, jalapeño e sour cream.', 34.9),
            ],
        )

    conn.commit()
    conn.close()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/health':
            self._send_json({'status': 'ok'})
            return

        if parsed.path == '/api/products':
            conn = get_connection()
            rows = conn.execute('SELECT id, name, description, price FROM products ORDER BY id').fetchall()
            conn.close()
            products = [dict(row) for row in rows]
            self._send_json(products)
            return

        if parsed.path.startswith('/api/orders/'):
            try:
                order_id = int(parsed.path.split('/')[-1])
            except ValueError:
                self._send_json({'error': 'ID inválido.'}, 400)
                return

            conn = get_connection()
            order = conn.execute(
                '''
                SELECT id, customer_name AS customerName, customer_phone AS customerPhone, total, created_at AS createdAt
                FROM orders
                WHERE id = ?
                ''',
                (order_id,),
            ).fetchone()

            if not order:
                conn.close()
                self._send_json({'error': 'Pedido não encontrado.'}, 404)
                return

            items = conn.execute(
                '''
                SELECT product_id AS productId, product_name AS productName, quantity, unit_price AS unitPrice, subtotal
                FROM order_items
                WHERE order_id = ?
                ''',
                (order_id,),
            ).fetchall()
            conn.close()

            self._send_json({**dict(order), 'items': [dict(item) for item in items]})
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path != '/api/orders':
            self._send_json({'error': 'Rota não encontrada.'}, 404)
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
        except (ValueError, json.JSONDecodeError):
            self._send_json({'error': 'JSON inválido.'}, 400)
            return

        customer_name = (data.get('customerName') or '').strip()
        customer_phone = (data.get('customerPhone') or '').strip()
        items = data.get('items')

        if not customer_name or not customer_phone or not isinstance(items, list) or len(items) == 0:
            self._send_json({'error': 'Dados do pedido inválidos.'}, 400)
            return

        conn = get_connection()

        try:
            normalized_items = []
            total = 0

            for item in items:
                product_id = item.get('productId')
                quantity = item.get('quantity')

                if not isinstance(product_id, int) or not isinstance(quantity, int) or quantity <= 0:
                    raise ValueError('Item inválido')

                product = conn.execute(
                    'SELECT id, name, price FROM products WHERE id = ?', (product_id,)
                ).fetchone()

                if not product:
                    raise ValueError('Produto não encontrado')

                subtotal = product['price'] * quantity
                total += subtotal
                normalized_items.append(
                    {
                        'product_id': product['id'],
                        'product_name': product['name'],
                        'quantity': quantity,
                        'unit_price': product['price'],
                        'subtotal': subtotal,
                    }
                )

            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO orders (customer_name, customer_phone, total) VALUES (?, ?, ?)',
                (customer_name, customer_phone, total),
            )
            order_id = cursor.lastrowid

            for item in normalized_items:
                cursor.execute(
                    '''
                    INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        order_id,
                        item['product_id'],
                        item['product_name'],
                        item['quantity'],
                        item['unit_price'],
                        item['subtotal'],
                    ),
                )

            conn.commit()
            self._send_json(
                {'orderId': order_id, 'total': total, 'message': 'Pedido criado com sucesso!'},
                201,
            )
        except ValueError:
            conn.rollback()
            self._send_json({'error': 'Item de pedido inválido.'}, 400)
        except Exception:
            conn.rollback()
            self._send_json({'error': 'Erro ao salvar pedido.'}, 500)
        finally:
            conn.close()


if __name__ == '__main__':
    initialize_database()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'Batata Shop rodando em http://localhost:{PORT}')
    server.serve_forever()
