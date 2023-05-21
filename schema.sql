drop table if exists Customer;
drop table if exists Order;
drop table if exists Sale;
drop table if exists pay;
drop table if exists Employee;
drop table if exists process;
drop table if exists Department;
drop table if exists Workplace;
drop table if exists Office;
drop table if exists Warehouse;
drop table if exists delivery;
drop table if exists works;
drop table if exists Product;
drop table if exists EAN_Product;
drop table if exists contains;
drop table if exists supply_contract;
drop table if exists supplier;



create table Customer (
    cust_no SERIAL,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(80) NOT NULL UNIQUE,
    phone VARCHAR(40) NOT NULL,
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY(cust_no)
);

create table Order (
   order_no SERIAL,
   date DATE NOT NULL,
   cust_no INTEGER NOT NULL,
   PRIMARY KEY(order_no),
   FOREIGN KEY(cust_no) REFERENCES Customer(cust_no)
);

create table Sale (
  order_no INTEGER NOT NULL,
  PRIMARY KEY(order_no),
  FOREIGN KEY(order_no) REFERENCES Order(order_no),
);

create table pay(
  order_no int NOT NULL,
  cust_no int NOT NULL,
  PRIMARY KEY(order_no),
  FOREIGN KEY(order_no) REFERENCES Order(order_no),
  FOREIGN KEY(cust_no) REFERENCES Customer(cust_no)
);

create table Employee(
  ssn INTEGER NOT NULL,
  TIN INTEGER NOT NULL UNIQUE,
  bdate DATE NOT NULL,
  name VARCHAR(80) NOT NULL,
  PRIMARY KEY (ssn)
);

create table process(
  ssn int NOT NULL,
  order_no int NOT NULL,
  PRIMARY KEY(ssn, order_no)
  FOREIGN KEY(ssn) REFERENCES Employee(ssn),
  FOREIGN KEY(order_no) REFERENCES Order(order_no),
);

create table Department(
  name VARCHAR(50),
  PRIMARY KEY(name),
);

create table Workplace(
  address VARCHAR(100)
  lat VARCHAR(20),
  long VARCHAR(20),
  PRIMARY KEY(address),
  UNIQUE(lat, long)
);

Create table Office(
  address VARCHAR(100),
  PRIMARY KEY(address),
  FOREIGN KEY(address) REFERENCES Workplace(address)
);

CREATE TABLE Warehouse(
  address VARCHAR(100),
  PRIMARY KEY(address),
  FOREIGN KEY(address) REFERENCES Workplace(address)
);

CREATE TABLE works(
  ssn INTEGER NOT NULL,
  name VARCHAR(50) NOT NULL,
  address VARCHAR(100) NOT NULL,
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
  sku INTEGER NOT NULL,
  ean VARCHAR(15) NOT NULL,
  PRIMARY KEY(sku),
  FOREIGN KEY(sku) REFERENCES Product(sku)
);

CREATE TABLE contains(
  sku INTEGER NOT NULL,
  order_no INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  PRIMARY KEY(sku, order_no),
  FOREIGN KEY(sku) REFERENCES Product(sku),
  FOREIGN KEY(order_no) REFERENCES Order(order_no)
);

CREATE TABLE Supplier(
  TIN INTEGER NOT NULL,
  name VARCHAR(80) NOT NULL,
  address VARCHAR(100) NOT NULL,
  PRIMARY KEY(TIN)
);

CREATE TABLE supply_contract(
  TIN INTEGER NOT NULL,
  sku INTEGER NOT NULL,
  PRIMARY KEY(TIN),
  FOREIGN KEY(TIN) REFERENCES Supplier(TIN),
  FOREIGN KEY(sku) REFERENCES Product(sku)
);

CREATE TABLE delivery(
  address VARCHAR(100),
  TIN INTEGER NOT NULL,
  PRIMARY KEY(address, TIN),  
  FOREIGN KEY(address) REFERENCES Warehouse(address),
  FOREIGN KEY(TIN) REFERENCES supply_contract(TIN)
);
