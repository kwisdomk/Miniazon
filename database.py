import sqlite3
import os

def init_database():
    """Init the db with mock data"""

    if os.path.exists('miniazon.db'): 
        os.remove('miniazon.db')
    conn = sqlite3.connect('miniazon.db')
    cursor = conn.cursor()

    #prod table
    cursor.execute('''
        CREATE TABLE products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   description TEXT,
                   price REAL,
                   category TEXT
                   )
            ''')
    sample_products = [
        ('Laptop', 'High-performance laptop for programming and gaming', 999.99, 'Electronics'),
        ('Wireless Mouse', 'Ergonomic wireless mouse with long battery life', 29.99, 'Electronics'),
        ('Mechanical Keyboard', 'RGB mechanical keyboard with blue switches', 79.99, 'Electronics'),
        ('Monitor', '27-inch 4K display for professional work', 399.99, 'Electronics'),
        ('Headphones', 'Noise-cancelling wireless headphones', 199.99, 'Electronics'),
        ('Webcam', '1080p HD webcam for video conferences', 49.99, 'Electronics'),
        ('Laptop Stand', 'Adjustable aluminum laptop stand', 39.99, 'Accessories'),
        ('USB-C Hub', '7-in-1 USB-C hub with HDMI and Ethernet', 35.99, 'Accessories')
    ]

    cursor.executemany(
        'INSERT INTO products (name, description, price, category) VALUES (?, ?, ?, ?)',
        sample_products)

    conn.commit()
    conn.close()
    print("Database initialized with mock data.")

if __name__ == '__main__':
    init_database()