DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS "order" CASCADE;
DROP TABLE IF EXISTS Sale CASCADE;
DROP TABLE IF EXISTS pay CASCADE;
DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS process CASCADE;
DROP TABLE IF EXISTS Department CASCADE;
DROP TABLE IF EXISTS Workplace CASCADE;
DROP TABLE IF EXISTS Office CASCADE;
DROP TABLE IF EXISTS Warehouse CASCADE;
DROP TABLE IF EXISTS delivery CASCADE;
DROP TABLE IF EXISTS works CASCADE;
DROP TABLE IF EXISTS Product CASCADE;
DROP TABLE IF EXISTS EAN_Product CASCADE;
DROP TABLE IF EXISTS contains CASCADE;
DROP TABLE IF EXISTS supply_contract CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;

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
); -- For each order, there must be an entry in the contains table with the same order_no

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
); -- Customers can only pay for orders they have made

CREATE TABLE Employee(
  ssn INTEGER,
  TIN INTEGER NOT NULL UNIQUE,
  bdate DATE NOT NULL,
  name VARCHAR(80) NOT NULL,
  PRIMARY KEY (ssn)
); -- For each employee, there must be an entry in the works table with the same ssn

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
); -- For each product, there must be an entry in the supply_contract table with the same sku

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
); -- For each supplier, there must be an entry in the supply_contract table with the same TIN

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
