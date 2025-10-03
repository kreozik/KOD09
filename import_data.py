import sqlite3
import csv

conn = sqlite3.connect('shoe_sales.db')
cursor = conn.cursor()

with open('database_schema.sql', 'r') as f:
    schema = f.read()
cursor.executescript(schema)

with open('sales_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

clients = {}
sellers = {}
warehouses = {}
products = {}
orders = {}

for row in data:
    email = row['Email клиента']
    cursor.execute('SELECT client_id FROM Clients WHERE email = ?', (email,))
    result = cursor.fetchone()
    if result:
        client_id = result[0]
    else:
        cursor.execute('INSERT INTO Clients (full_name, email, phone) VALUES (?, ?, ?)',
                       (row['ФИО Клиента'], email, row['Телефон клиента']))
        client_id = cursor.lastrowid
    clients[email] = client_id

for row in data:
    key = (row['ФИО продавца'], row['Должность продавца'])
    if key not in sellers:
        cursor.execute('INSERT INTO Sellers (full_name, position) VALUES (?, ?)',
                       (row['ФИО продавца'], row['Должность продавца']))
        sellers[key] = cursor.lastrowid

for row in data:
    key = (row['Склад отгрузки'], row['Адрес склада'], int(row['Вместимость склада']), int(row['Количество полок']))
    if key not in warehouses:
        cursor.execute('INSERT INTO Warehouses (name, address, capacity, shelves) VALUES (?, ?, ?, ?)',
                       (row['Склад отгрузки'], row['Адрес склада'], int(row['Вместимость склада']), int(row['Количество полок'])))
        warehouses[key] = cursor.lastrowid

for row in data:
    key = (row['Название модели'], row['Категория обуви'], row['Производитель'], int(row['Размер обуви']), row['Цвет'], float(row['Цена за пару']))
    if key not in products:
        cursor.execute('INSERT INTO Products (model_name, category, manufacturer, size, color, price_per_pair) VALUES (?, ?, ?, ?, ?, ?)',
                       (row['Название модели'], row['Категория обуви'], row['Производитель'], int(row['Размер обуви']), row['Цвет'], float(row['Цена за пару'])))
        products[key] = cursor.lastrowid

for row in data:
    order_num = int(row['Номер заказа'])
    if order_num not in orders:
        client_email = row['Email клиента']
        client_id = clients[client_email]
        cursor.execute('INSERT INTO Orders (order_number, order_date, client_id) VALUES (?, ?, ?)',
                       (order_num, row['Дата заказа'], client_id))
        orders[order_num] = cursor.lastrowid

for row in data:
    order_num = int(row['Номер заказа'])
    order_id = orders[order_num]
    product_key = (row['Название модели'], row['Категория обуви'], row['Производитель'], int(row['Размер обуви']), row['Цвет'], float(row['Цена за пару']))
    product_id = products[product_key]
    seller_key = (row['ФИО продавца'], row['Должность продавца'])
    seller_id = sellers[seller_key]
    warehouse_key = (row['Склад отгрузки'], row['Адрес склада'], int(row['Вместимость склада']), int(row['Количество полок']))
    warehouse_id = warehouses[warehouse_key]
    quantity = int(row['Кол-во пар'])
    cursor.execute('INSERT INTO OrderItems (order_id, product_id, quantity, seller_id, warehouse_id) VALUES (?, ?, ?, ?, ?)',
                   (order_id, product_id, quantity, seller_id, warehouse_id))

conn.commit()
conn.close()

print("Data imported successfully into shoe_sales.db")
