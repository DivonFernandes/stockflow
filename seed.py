import sqlite3
import os
from database import get_db_connection

def seed_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if entries table is empty
    cursor.execute("SELECT COUNT(*) FROM entries")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Semeando banco de dados com dados de teste...")
        
        # Test entries
        entries = [
            ('2026-05-10', 'SATA', 'Kingston A400', '240GB', 10, 'Distribuidora Master', 139.90),
            ('2026-05-12', 'SATA', 'Crucial BX500', '480GB', 15, 'TechImports', 229.00),
            ('2026-05-15', 'NVMe', 'XPG Gammix S70', '1TB', 8, 'Pichau Atacado', 450.00),
            ('2026-05-18', 'NVMe', 'Samsung 980 Pro', '2TB', 5, 'Kabum Corp', 850.00)
        ]
        
        cursor.executemany("""
            INSERT INTO entries (entry_date, ssd_type, brand, size, quantity, supplier, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, entries)
        
        # Test exits
        exits = [
            ('2026-05-14', 'SATA', 'Kingston A400', '240GB', 3, 'Distribuidora Master', 'Carlos Eduardo'),
            ('2026-05-20', 'NVMe', 'XPG Gammix S70', '1TB', 2, 'Pichau Atacado', 'Ana Beatriz'),
            ('2026-05-22', 'SATA', 'Crucial BX500', '480GB', 12, 'TechImports', 'Escola Alfa')
        ]
        
        cursor.executemany("""
            INSERT INTO exits (exit_date, ssd_type, brand, size, quantity, supplier, client)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, exits)
        
        # Test aggregated products
        products = [
            ('SATA', 'Kingston A400', '240GB', 7, 3), # 10 - 3
            ('SATA', 'Crucial BX500', '480GB', 3, 12), # 15 - 12 (triggers low stock)
            ('NVMe', 'XPG Gammix S70', '1TB', 6, 2), # 8 - 2
            ('NVMe', 'Samsung 980 Pro', '2TB', 5, 0)  # 5 - 0
        ]
        
        cursor.executemany("""
            INSERT INTO products (ssd_type, brand, size, quantity, total_exited)
            VALUES (?, ?, ?, ?, ?)
        """, products)
        
        conn.commit()
        print("Banco de dados semeado com sucesso.")
    else:
        print("O banco de dados já possui dados, pulando semeadura.")
        
    conn.close()

if __name__ == '__main__':
    seed_data()
