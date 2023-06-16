DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS pay CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS process CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS workplace CASCADE;
DROP TABLE IF EXISTS works CASCADE;
DROP TABLE IF EXISTS office CASCADE;
DROP TABLE IF EXISTS warehouse CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS contains CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS delivery CASCADE;

/* Change this above */



CREATE TABLE customer(
  cust_no INTEGER PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  email VARCHAR(254) UNIQUE NOT NULL,
  phone VARCHAR(15),
  address VARCHAR(255)
);

CREATE TABLE orders(
  order_no INTEGER PRIMARY KEY,
  cust_no INTEGER NOT NULL REFERENCES customer,
  date DATE NOT NULL
  --order_no must exist in contains
);

CREATE TABLE pay(
  order_no INTEGER PRIMARY KEY REFERENCES orders,
  cust_no INTEGER NOT NULL REFERENCES customer
);

CREATE TABLE employee(
  ssn VARCHAR(20) PRIMARY KEY,
  TIN VARCHAR(20) UNIQUE NOT NULL,
  bdate DATE,
  name VARCHAR NOT NULL
  --age must be >=18
);

CREATE TABLE process(
  ssn VARCHAR(20) REFERENCES employee,
  order_no INTEGER REFERENCES orders,
  PRIMARY KEY (ssn, order_no)
);

CREATE TABLE department(
  name VARCHAR PRIMARY KEY
);

CREATE TABLE workplace(
  address VARCHAR PRIMARY KEY,
  lat NUMERIC(8, 6) NOT NULL,
  long NUMERIC(9, 6) NOT NULL,
  UNIQUE(lat, long)
  --address must be in warehouse or office but not both
);

CREATE TABLE office(
  address VARCHAR(255) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE warehouse(
  address VARCHAR(255) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE works(
  ssn VARCHAR(20) REFERENCES employee,
  name VARCHAR(200) REFERENCES department,
  address VARCHAR(255) REFERENCES workplace,
  PRIMARY KEY (ssn, name, address)
);

CREATE TABLE product(
  SKU VARCHAR(25) PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  description VARCHAR,
  price NUMERIC(10, 2) NOT NULL,
  ean NUMERIC(13) UNIQUE
);

CREATE TABLE contains(
  order_no INTEGER REFERENCES orders,
  SKU VARCHAR(25) REFERENCES product,
  qty INTEGER,
  PRIMARY KEY (order_no, SKU)
);

CREATE TABLE supplier(
  TIN VARCHAR(20) PRIMARY KEY,
  name VARCHAR(200),
  address VARCHAR(255),
  SKU VARCHAR(25) REFERENCES product,
  date DATE
);

CREATE TABLE delivery(
  address VARCHAR(255) REFERENCES warehouse ,
  TIN VARCHAR(20) REFERENCES supplier,
  PRIMARY KEY (address, TIN)
);

insert into customer (cust_no, name, email, phone, address) VALUES (-1,'Deleted_User', '', '', '');
insert into customer (cust_no, name, email, phone, address) VALUES (1,'Belchior', 'belchiorlindo@gmail.com', '912345678', 'Avenida da Liberdade, 2000-002 Póvoa de Varzim');
insert into customer (cust_no, name, email, phone, address) VALUES (2,'Nunes', 'danielnunes@gmail.com', '939393939', 'Travessa dos Pescadores, 3000-003 Coimbra');
insert into customer (cust_no, name, email, phone, address) VALUES (3,'Costa', 'joaolscosta@gmail.com', '947854684', 'Rua das Flores, 1000-001 Lisboa');


insert into orders (order_no, date, cust_no) VALUES (1,'2017-01-01', (select cust_no from customer where name = 'Belchior'));
insert into orders (order_no, date, cust_no) VALUES (2,'2018-01-01', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (3,'2019-01-01', (select cust_no from customer where name = 'Costa'));
insert into orders (order_no, date, cust_no) VALUES (4,'2014-01-01', (select cust_no from customer where name = 'Costa'));
insert into orders (order_no, date, cust_no) VALUES (5,'2023-01-02', (select cust_no from customer where name = 'Costa'));
insert into orders (order_no, date, cust_no) VALUES (6,'2023-02-02', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (7,'2023-01-03', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (8,'2022-01-03', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (9,'2022-01-04', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (10,'2022-01-04', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (11,'2022-03-04', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (12,'2022-10-04', (select cust_no from customer where name = 'Nunes'));




insert into pay (order_no, cust_no) VALUES ((select order_no from orders where date = '2017-01-01'), (select cust_no from customer where name = 'Belchior'));
insert into pay (order_no, cust_no) VALUES ((select order_no from orders where date = '2018-01-01'), (select cust_no from customer where name = 'Nunes'));
insert into pay (order_no, cust_no) VALUES (8, 2);
insert into pay (order_no, cust_no) VALUES (9, 2);

insert into employee (ssn, TIN, bdate, name) VALUES ('546654654', '123123123', '2002-04-10', 'Pedrinho');
insert into employee (ssn, TIN, bdate, name) VALUES ('546654655', '123123124', '2002-02-14', 'Gui');
insert into employee (ssn, TIN, bdate, name) VALUES ('546654656', '123123125', '2002-01-01', 'Luana');

insert into process (ssn, order_no) VALUES ((select ssn from employee where name = 'Pedrinho'), (select order_no from orders where date = '2017-01-01'));
insert into process (ssn, order_no) VALUES ((select ssn from employee where name = 'Luana'), (select order_no from orders where date = '2023-01-02'));
insert into process (ssn, order_no) VALUES ((select ssn from employee where name = 'Gui'), (select order_no from orders where date = '2019-01-01'));
insert into process (ssn, order_no) VALUES ((select ssn from employee where name = 'Gui'), (select order_no from orders where date = '2023-01-03'));
insert into process (ssn, order_no) VALUES ((select ssn from employee where name = 'Pedrinho'), (select order_no from orders where date = '2014-01-01'));
insert into process (ssn, order_no) VALUES ((select ssn from employee where name = 'Gui'), 11);
insert into process (ssn, order_no) VALUES ((select ssn from employee where name = 'Gui'), 12);


insert into department (name) VALUES ('Marketing');
insert into department (name) VALUES ('Production');

insert into workplace (address, lat, long) VALUES ('Rua das Flores, 1000-001 Lisboa', '12.000000', '45.000000');
insert into workplace (address, lat, long) VALUES ('Rua do Comércio, 4000-004 Porto', '78.000000', '10.000000');
insert into workplace (address, lat, long) VALUES ('Praça da República, 5000-005 Vila Real', '78.000000', '13.000000');
insert into workplace (address, lat, long) VALUES ('Avenida Central, 6000-006 Castelo Branco', '78.000000', '11.000000');


insert into office (address) VALUES ((select address from workplace where address = 'Praça da República, 5000-005 Vila Real'));
insert into office (address) VALUES ((select address from workplace where address = 'Avenida Central, 6000-006 Castelo Branco'));

insert into warehouse (address) VALUES ((select address from workplace where address = 'Rua das Flores, 1000-001 Lisboa'));
insert into warehouse (address) VALUES ((select address from workplace where address = 'Rua do Comércio, 4000-004 Porto'));


insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Pedrinho'), (select name from department where name = 'Marketing'), (select address from workplace where address = 'Praça da República, 5000-005 Vila Real'));
insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Luana'), (select name from department where name = 'Marketing'), (select address from workplace where address = 'Rua das Flores, 1000-001 Lisboa'));
insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Gui'), (select name from department where name = 'Production'), (select address from workplace where address = 'Rua das Flores, 1000-001 Lisboa'));
insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Gui'), (select name from department where name = 'Production'), (select address from workplace where address = 'Avenida Central, 6000-006 Castelo Branco'));


insert into product (SKU, name, description, price, ean) VALUES ('-1', '', '',0, '-1');
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS011', 'Gaming Chair', 'Chair made with love and kindness', 5.35, '1234567891234');
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS012', 'Cake', 'Cake made by our amazing chef Luana', 10.35, '1234567891235');
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS013', 'TV', 'LG TV 4K', 500.35, '1234567891236');
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS014', 'Table', 'Table made with paus and cola', 50.35, '1234567891237');



insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'Gaming Chair'), (select order_no from orders where date = '2017-01-01'), 2);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'Cake'), (select order_no from orders where date = '2018-01-01'), 10);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), (select order_no from orders where date = '2019-01-01'), 3);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), (select order_no from orders where date = '2023-01-02'), 14);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), (select order_no from orders where date = '2023-01-03'), 3);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 8, 14);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 9, 20);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 10, 2);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 11, 2);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 12, 2);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 4, 14);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 6, 14);


insert into supplier (TIN, name, address, SKU, date) VALUES ('123456789', 'Goncalo', 'Rua das Palmeiras, 7000-007 Évora', (select SKU from product where name = 'Gaming Chair'), '2017-01-01');
insert into supplier (TIN, name, address, SKU, date) VALUES ('123456788', 'Rafael', 'Avenida do Mar, 8000-008 Faro', (select SKU from product where name = 'Cake'), '2018-01-01');
insert into supplier (TIN, name, address, SKU, date) VALUES ('123456787', 'Luana', 'Travessa das Oliveiras, 9000-009 Funchal', (select SKU from product where name = 'TV'), '2019-01-01');
insert into supplier (TIN, name, address, SKU, date) VALUES ('123456786', 'Ricky', 'Rua dos Castanheiros, 1000-010 Guarda', (select SKU from product where name = 'TV'), '2023-01-02');



insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua das Flores, 1000-001 Lisboa'), (select TIN from supplier where name = 'Goncalo'));
insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua do Comércio, 4000-004 Porto'), (select TIN from supplier where name = 'Luana'));
insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua das Flores, 1000-001 Lisboa'), (select TIN from supplier where name = 'Rafael'));
insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua do Comércio, 4000-004 Porto'), (select TIN from supplier where name = 'Ricky'));

--R1:
CREATE OR REPLACE FUNCTION ValidAge() RETURNS TRIGGER AS
$$
  BEGIN
    IF ((CURRENT_DATE - 6570) < NEW.bdate ) THEN
      RAISE EXCEPTION 'Employees must be 18 years old';
    END IF;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;

CREATE TRIGGER CheckValidAge
BEFORE INSERT OR UPDATE ON employee
FOR EACH ROW EXECUTE PROCEDURE ValidAge();




-- R2:
CREATE OR REPLACE FUNCTION CheckValidWorkplace() RETURNS TRIGGER AS
$$
  BEGIN
    IF (NEW.address NOT IN (SELECT address FROM Office) AND
        NEW.address NOT IN (SELECT address FROM Warehouse)) 
      OR
       ( NEW.address IN (SELECT address FROM Office) AND
         NEW.address IN (SELECT address FROM Warehouse))  
      THEN
      RAISE EXCEPTION 'Workplace must be either an Office or a Warehouse and not Both!';
    END IF;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;

CREATE TRIGGER CheckValidWorkplace
BEFORE INSERT OR UPDATE ON Workplace
FOR EACH ROW EXECUTE FUNCTION CheckValidWorkplace();

-- R3:
CREATE OR REPLACE FUNCTION CheckValidOrder() RETURNS TRIGGER AS
$$
  BEGIN
    IF (NEW.order_no NOT IN (SELECT order_no FROM contains)) THEN
      RAISE EXCEPTION 'Orders must have at least one product!';
    END IF;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER CheckValidOrder
AFTER INSERT OR UPDATE ON orders 
DEFERRABLE 
INITIALLY DEFERRED
FOR EACH ROW EXECUTE PROCEDURE CheckValidOrder();
