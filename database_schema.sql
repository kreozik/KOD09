DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Clients;
DROP TABLE IF EXISTS Sellers;
DROP TABLE IF EXISTS Warehouses;

PRAGMA foreign_keys = ON;

CREATE TABLE Clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE Sellers (
    seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT UNIQUE NOT NULL,
    position TEXT NOT NULL
);

CREATE TABLE Warehouses (
    warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    address TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    shelves INTEGER NOT NULL
);

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    category TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    size INTEGER NOT NULL,
    color TEXT NOT NULL,
    price_per_pair REAL NOT NULL
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number INTEGER UNIQUE NOT NULL,
    order_date TEXT NOT NULL,
    client_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);

CREATE TABLE OrderItems (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
);
