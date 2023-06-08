insert into customer (cust_no, name, email, phone, address) VALUES (1,'Belchior', 'belchiorlindo@gmail.com', '912345678', 'Avenida da Liberdade, 2000-002 Santarém');
insert into customer (cust_no, name, email, phone, address) VALUES (2,'Nunes', 'danielnunes@gmail.com', '939393939', 'Travessa dos Pescadores, 3000-003 Coimbra');
insert into customer (cust_no, name, email, phone, address) VALUES (3,'Costa', 'joaolscosta@gmail.com', '947854684', 'Rua das Flores, 1000-001 Lisboa');

/* será que tem de ter o order_no????????*/
insert into orders (order_no, date, cust_no) VALUES (4,'2017-01-01', (select cust_no from customer where name = 'Belchior'));
insert into orders (order_no, date, cust_no) VALUES (5,'2018-01-01', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (6,'2019-01-01', (select cust_no from customer where name = 'Costa'));
insert into orders (order_no, date, cust_no) VALUES (7,'2014-01-01', (select cust_no from customer where name = 'Costa'));
insert into orders (order_no, date, cust_no) VALUES (8,'2023-01-02', (select cust_no from customer where name = 'Costa'));
insert into orders (order_no, date, cust_no) VALUES (9,'2023-02-02', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (10,'2023-01-03', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (11,'2022-01-03', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (12,'2022-01-04', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (13,'2022-01-04', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (14,'2022-03-04', (select cust_no from customer where name = 'Nunes'));
insert into orders (order_no, date, cust_no) VALUES (15,'2022-10-04', (select cust_no from customer where name = 'Nunes'));


/*
insert into sale (order_no) VALUES ((select order_no from "order" where date = '2017-01-01'));
insert into sale (order_no) VALUES ((select order_no from "order" where date = '2018-01-01'));
*/

insert into pay (order_no, cust_no) VALUES ((select order_no from orders where date = '2017-01-01'), (select cust_no from customer where name = 'Belchior'));
insert into pay (order_no, cust_no) VALUES ((select order_no from orders where date = '2018-01-01'), (select cust_no from customer where name = 'Nunes'));
insert into pay (order_no, cust_no) VALUES (11, 2);
insert into pay (order_no, cust_no) VALUES (12, 2);

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

/*
insert into department (name) VALUES ('Sales');
*/
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

/*mudei o referencies do address pro que ta no schema, nao tenho a certeza*/
insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Pedrinho'), (select name from department where name = 'Marketing'), (select address from workplace where address = 'Praça da República, 5000-005 Vila Real'));
insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Luana'), (select name from department where name = 'Marketing'), (select address from workplace where address = 'Rua das Flores, 1000-001 Lisboa'));
insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Gui'), (select name from department where name = 'Production'), (select address from workplace where address = 'Rua das Flores, 1000-001 Lisboa'));
insert into works (ssn, name, address) VALUES ((select ssn from employee where name = 'Gui'), (select name from department where name = 'Production'), (select address from workplace where address = 'Avenida Central, 6000-006 Castelo Branco'));

/* nao tenho a certeza do sku */
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS011', 'Gaming Chair', 'Chair made with love and kindness', 5.35, '1234567891234');
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS012', 'Cake', 'Cake made by our amazing chef Luana', 10.35, '1234567891235');
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS013', 'TV', 'LG TV 4K', 500.35, '1234567891236');
insert into product (SKU, name, description, price, ean) VALUES ('EI01TS01EI01TS01EI01TS014', 'Table', 'Table made with paus and cola', 50.35, '1234567891237');

/*
insert into EAN_Product (sku, ean) VALUES ((select sku from Product where name = 'Gaming Chair'), '1234567891234');
insert into EAN_Product (sku, ean) VALUES ((select sku from Product where name = 'Cake'), '1234567891235');
insert into EAN_Product (sku, ean) VALUES ((select sku from Product where name = 'TV'), '1234567891236');
*/

insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'Gaming Chair'), (select order_no from orders where date = '2017-01-01'), 2);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'Cake'), (select order_no from orders where date = '2018-01-01'), 10);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), (select order_no from orders where date = '2019-01-01'), 3);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), (select order_no from orders where date = '2023-01-02'), 14);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), (select order_no from orders where date = '2023-01-03'), 3);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 11, 14);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 12, 20);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 13, 2);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 14, 2);
insert into contains (SKU, order_no, qty) VALUES ((select SKU from product where name = 'TV'), 15, 2);


insert into supplier (TIN, name, address, SKU, date) VALUES ('123456789', 'Goncalo', 'Rua das Palmeiras, 7000-007 Évora', (select SKU from product where name = 'Gaming Chair'), '2017-01-01');
insert into supplier (TIN, name, address, SKU, date) VALUES ('123456788', 'Rafael', 'Avenida do Mar, 8000-008 Faro', (select SKU from product where name = 'Cake'), '2018-01-01');
insert into supplier (TIN, name, address, SKU, date) VALUES ('123456787', 'Luana', 'Travessa das Oliveiras, 9000-009 Funchal', (select SKU from product where name = 'TV'), '2019-01-01');
insert into supplier (TIN, name, address, SKU, date) VALUES ('123456786', 'Ricky', 'Rua dos Castanheiros, 1000-010 Guarda', (select SKU from product where name = 'TV'), '2023-01-02');

/*
insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Goncalo'), (select sku from Product where name = 'Gaming Chair'));
insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Luana'), (select sku from Product where name = 'Cake'));
insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Rafael'), (select sku from Product where name = 'TV'));
insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Ricky'), (select sku from Product where name = 'Table'));
*/

insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua das Flores, 1000-001 Lisboa'), (select TIN from supplier where name = 'Goncalo'));
insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua do Comércio, 4000-004 Porto'), (select TIN from supplier where name = 'Luana'));
insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua das Flores, 1000-001 Lisboa'), (select TIN from supplier where name = 'Rafael'));
insert into delivery (address, TIN) VALUES ((select address from warehouse where address = 'Rua do Comércio, 4000-004 Porto'), (select TIN from supplier where name = 'Ricky'));
