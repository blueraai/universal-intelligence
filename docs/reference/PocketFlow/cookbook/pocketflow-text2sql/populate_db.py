import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_FILE = "ecommerce.db"

def populate_database(db_file=DB_FILE):
    """Creates and populates the SQLite database."""
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing database: {db_file}")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create Tables
    cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        registration_date DATE NOT NULL,
        city TEXT,
        country TEXT DEFAULT 'USA'
    );
    """)
    print("Created 'customers' table.")

    cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL,
        price REAL NOT NULL CHECK (price > 0),
        stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0)
    );
    """)
    print("Created 'products' table.")

    cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
        total_amount REAL,
        shipping_address TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );
    """)
    print("Created 'orders' table.")

    cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        price_per_unit REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    );
    """)
    print("Created 'order_items' table.")

    # Insert Sample Data
    customers_data = [
        ('Alice', 'Smith', 'alice.s@email.com', '2023-01-15', 'New York', 'USA'),
        ('Bob', 'Johnson', 'b.johnson@email.com', '2023-02-20', 'Los Angeles', 'USA'),
        ('Charlie', 'Williams', 'charlie.w@email.com', '2023-03-10', 'Chicago', 'USA'),
        ('Diana', 'Brown', 'diana.b@email.com', '2023-04-05', 'Houston', 'USA'),
        ('Ethan', 'Davis', 'ethan.d@email.com', '2023-05-12', 'Phoenix', 'USA'),
        ('Fiona', 'Miller', 'fiona.m@email.com', '2023-06-18', 'Philadelphia', 'USA'),
        ('George', 'Wilson', 'george.w@email.com', '2023-07-22', 'San Antonio', 'USA'),
        ('Hannah', 'Moore', 'hannah.m@email.com', '2023-08-30', 'San Diego', 'USA'),
        ('Ian', 'Taylor', 'ian.t@email.com', '2023-09-05', 'Dallas', 'USA'),
        ('Julia', 'Anderson', 'julia.a@email.com', '2023-10-11', 'San Jose', 'USA')
    ]
    cursor.executemany("INSERT INTO customers (first_name, last_name, email, registration_date, city, country) VALUES (?, ?, ?, ?, ?, ?)", customers_data)
    print(f"Inserted {len(customers_data)} customers.")

    products_data = [
        ('Laptop Pro', 'High-end laptop for professionals', 'Electronics', 1200.00, 50),
        ('Wireless Mouse', 'Ergonomic wireless mouse', 'Accessories', 25.50, 200),
        ('Mechanical Keyboard', 'RGB backlit mechanical keyboard', 'Accessories', 75.00, 150),
        ('4K Monitor', '27-inch 4K UHD Monitor', 'Electronics', 350.00, 80),
        ('Smartphone X', 'Latest generation smartphone', 'Electronics', 999.00, 120),
        ('Coffee Maker', 'Drip coffee maker', 'Home Goods', 50.00, 300),
        ('Running Shoes', 'Comfortable running shoes', 'Apparel', 90.00, 250),
        ('Yoga Mat', 'Eco-friendly yoga mat', 'Sports', 30.00, 400),
        ('Desk Lamp', 'Adjustable LED desk lamp', 'Home Goods', 45.00, 180),
        ('Backpack', 'Durable backpack for travel', 'Accessories', 60.00, 220)
    ]
    cursor.executemany("INSERT INTO products (name, description, category, price, stock_quantity) VALUES (?, ?, ?, ?, ?)", products_data)
    print(f"Inserted {len(products_data)} products.")

    orders_data = []
    start_date = datetime.now() - timedelta(days=60)
    order_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    for i in range(1, 21): # Create 20 orders
        customer_id = random.randint(1, 10)
        order_date = start_date + timedelta(days=random.randint(0, 59), hours=random.randint(0, 23))
        status = random.choice(order_statuses)
        shipping_address = f"{random.randint(100, 999)} Main St, Anytown"
        orders_data.append((customer_id, order_date.strftime('%Y-%m-%d %H:%M:%S'), status, None, shipping_address)) # Total amount calculated later

    cursor.executemany("INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_address) VALUES (?, ?, ?, ?, ?)", orders_data)
    print(f"Inserted {len(orders_data)} orders.")

    order_items_data = []
    order_totals = {} # Keep track of totals per order
    for order_id in range(1, 21):
        num_items = random.randint(1, 4)
        order_total = 0
        for _ in range(num_items):
            product_id = random.randint(1, 10)
            quantity = random.randint(1, 5)
            # Get product price
            cursor.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
            price_per_unit = cursor.fetchone()[0]
            order_items_data.append((order_id, product_id, quantity, price_per_unit))
            order_total += quantity * price_per_unit
        order_totals[order_id] = round(order_total, 2)

    cursor.executemany("INSERT INTO order_items (order_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)", order_items_data)
    print(f"Inserted {len(order_items_data)} order items.")

    # Update order totals
    for order_id, total_amount in order_totals.items():
        cursor.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", (total_amount, order_id))
    print("Updated order totals.")

    conn.commit()
    conn.close()
    print(f"Database '{db_file}' created and populated successfully.")

if __name__ == "__main__":
    populate_database()