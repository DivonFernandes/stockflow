import sqlite3
import os
import shutil
import tempfile
from werkzeug.security import generate_password_hash

class TursoRow(dict):
    """Dict wrapper that also supports index-based lookup like sqlite3.Row."""
    def __init__(self, keys, values):
        super().__init__(zip(keys, values))
        self._values = list(values)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._values[item]
        return super().__getitem__(item)

class TursoDBCursor:
    def __init__(self, client):
        self.client = client
        self._results = []
        self._index = 0

    def execute(self, sql, params=()):
        if isinstance(params, (list, tuple)):
            param_list = list(params)
        elif params is None:
            param_list = []
        else:
            param_list = [params]
            
        res = self.client.execute(sql, param_list)
        cols = res.columns
        self._results = [TursoRow(cols, row) for row in res.rows]
        self._index = 0
        return self

    def executemany(self, sql, params_list):
        for params in params_list:
            self.execute(sql, params)
        return self

    def fetchone(self):
        if self._index < len(self._results):
            row = self._results[self._index]
            self._index += 1
            return row
        return None

    def fetchall(self):
        rows = self._results[self._index:]
        self._index = len(self._results)
        return rows

class TursoDBConnection:
    def __init__(self, url, auth_token):
        import libsql_client
        # Ensure HTTPS scheme for serverless HTTP request execution
        if url.startswith('libsql://'):
            url = url.replace('libsql://', 'https://')
        self.client = libsql_client.create_client_sync(url=url, auth_token=auth_token)

    def cursor(self):
        return TursoDBCursor(self.client)

    def commit(self):
        pass  # Auto-committed by Turso over HTTP

    def close(self):
        if hasattr(self.client, 'close'):
            try:
                self.client.close()
            except Exception:
                pass

ROOT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stock.db')

def get_db_path():
    # On Vercel or read-only environment, copy DB to system temp dir (/tmp on Vercel/Linux)
    if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV') or not os.access(os.path.dirname(ROOT_DB_PATH), os.W_OK):
        temp_dir = tempfile.gettempdir()
        tmp_db = os.path.join(temp_dir, 'stock.db')
        if not os.path.exists(tmp_db):
            if os.path.exists(ROOT_DB_PATH):
                try:
                    shutil.copy2(ROOT_DB_PATH, tmp_db)
                except Exception as e:
                    print(f"Erro ao copiar banco para diretório temporário: {e}")
        return tmp_db
    return ROOT_DB_PATH

def get_db_connection():
    url = os.environ.get('TURSO_DATABASE_URL')
    token = os.environ.get('TURSO_AUTH_TOKEN')
    
    if url:
        return TursoDBConnection(url, token)
    else:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ssd_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            size TEXT,
            quantity INTEGER DEFAULT 0,
            total_exited INTEGER DEFAULT 0,
            UNIQUE(ssd_type, brand, size)
        )
    ''')
    
    # Create entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            ssd_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            size TEXT,
            quantity INTEGER NOT NULL,
            supplier TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # Create exits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exit_date TEXT NOT NULL,
            ssd_type TEXT NOT NULL,
            brand TEXT NOT NULL,
            size TEXT,
            quantity INTEGER NOT NULL,
            supplier TEXT NOT NULL,
            client TEXT NOT NULL
        )
    ''')
    
    # Check if admin user exists, if not create it
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    if not admin:
        hashed_password = generate_password_hash('admin')
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_password))
        print("Usuário 'admin' criado com sucesso.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado.")
