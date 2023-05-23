DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS "order";
DROP TABLE IF EXISTS Sale;
DROP TABLE IF EXISTS pay;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS process;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Workplace;
DROP TABLE IF EXISTS Office;
DROP TABLE IF EXISTS Warehouse;
DROP TABLE IF EXISTS delivery;
DROP TABLE IF EXISTS works;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS EAN_Product;
DROP TABLE IF EXISTS contains;
DROP TABLE IF EXISTS supply_contract;
DROP TABLE IF EXISTS supplier;

/* Change this above */



CREATE TABLE Customer (
    cust_no SERIAL,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(80) NOT NULL UNIQUE,
    phone VARCHAR(40) NOT NULL,
    address VARCHAR(255),
    PRIMARY KEY(cust_no)
);

CREATE TABLE "order" (
   order_no SERIAL,
   date DATE NOT NULL,
   cust_no INTEGER NOT NULL,
   PRIMARY KEY(order_no),
   FOREIGN KEY(cust_no) REFERENCES Customer(cust_no)
);

CREATE TABLE Sale (
  order_no INTEGER,
  PRIMARY KEY(order_no),
  FOREIGN KEY(order_no) REFERENCES "order"(order_no) ON DELETE CASCADE
);

CREATE TABLE pay(
  order_no INTEGER,
  cust_no INTEGER NOT NULL,
  PRIMARY KEY(order_no),
  FOREIGN KEY(order_no) REFERENCES "order"(order_no),
  FOREIGN KEY(cust_no) REFERENCES Customer(cust_no)
);

CREATE TABLE Employee(
  ssn INTEGER,
  TIN INTEGER NOT NULL UNIQUE,
  bdate DATE NOT NULL,
  name VARCHAR(80) NOT NULL,
  PRIMARY KEY (ssn)
);

CREATE TABLE process(
  ssn INTEGER,
  order_no INTEGER,
  PRIMARY KEY(ssn, order_no),
  FOREIGN KEY(ssn) REFERENCES Employee(ssn),
  FOREIGN KEY(order_no) REFERENCES "order"(order_no)
);

CREATE TABLE Department(
  name VARCHAR(50),
  PRIMARY KEY(name)
);

CREATE TABLE Workplace(
  address VARCHAR(100),
  lat VARCHAR(20) NOT NULL,
  long VARCHAR(20) NOT NULL,
  PRIMARY KEY(address),
  UNIQUE(lat, long)
);

Create TABLE Office(
  address VARCHAR(100),
  PRIMARY KEY(address),
  FOREIGN KEY(address) REFERENCES Workplace(address) ON DELETE CASCADE
);

CREATE TABLE Warehouse(
  address VARCHAR(100),
  PRIMARY KEY(address),
  FOREIGN KEY(address) REFERENCES Workplace(address) ON DELETE CASCADE
);

CREATE TABLE works(
  ssn INTEGER,
  name VARCHAR(50),
  address VARCHAR(100),
  PRIMARY KEY(ssn, name, address),
  FOREIGN KEY(ssn) REFERENCES Employee(ssn),
  FOREIGN KEY(name) REFERENCES Department(name), 
  FOREIGN KEY(address) REFERENCES Workplace(address)
);

CREATE TABLE Product(
  sku SERIAL,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY(sku)
);

CREATE TABLE EAN_Product(
  sku INTEGER,
  ean VARCHAR(15) NOT NULL UNIQUE,
  PRIMARY KEY(sku),
  FOREIGN KEY(sku) REFERENCES Product(sku) ON DELETE CASCADE
);

CREATE TABLE contains(
  sku INTEGER,
  order_no INTEGER,
  quantity INTEGER NOT NULL,
  PRIMARY KEY(sku, order_no),
  FOREIGN KEY(sku) REFERENCES Product(sku),
  FOREIGN KEY(order_no) REFERENCES "order"(order_no)
);

CREATE TABLE Supplier(
  TIN INTEGER,
  name VARCHAR(80) NOT NULL,
  address VARCHAR(100) NOT NULL,
  PRIMARY KEY(TIN)
);

CREATE TABLE supply_contract(
  TIN INTEGER,
  sku INTEGER NOT NULL,
  PRIMARY KEY(TIN),
  FOREIGN KEY(TIN) REFERENCES Supplier(TIN),
  FOREIGN KEY(sku) REFERENCES Product(sku)
);

CREATE TABLE delivery(
  address VARCHAR(100),
  TIN INTEGER,
  PRIMARY KEY(address, TIN),  
  FOREIGN KEY(address) REFERENCES Workplace(address),
  FOREIGN KEY(TIN) REFERENCES supply_contract(TIN)
);


/* 

ON DELETE CASCADE - se dermos delete em algum dado da tabela pai, esse
dado correspondente na tabela filho também vai ser removido

ON DELETE SET NULL - quando removido da tabela pai, na filho fica esse dado
correspondente set a null.

https://www.youtube.com/watch?v=PlZuYejVU3Q&t=9s

Supostamente temos que usar nas tabelas filho para eliminar o conteudo dela
indicando a tabela pai que contém essa FK.



*/