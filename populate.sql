insert into Customer (name, email, phone, address) VALUES ('Belchior', 'belchiorlindo@gmail.com', '912345678', 'Rua do Belchior');
insert into Customer (name, email, phone, address) VALUES ('Nunes', 'danielnunes@gmail.com', '939393939', 'Rua do Nunes');
insert into Customer (name, email, phone, address) VALUES ('Costa', 'joaolscosta@gmail.com', '947854684', 'Rua das flores');

insert into "order" (date, cust_no) VALUES ('2017-01-01', (select cust_no from Customer where name = 'Belchior'));
insert into "order" (date, cust_no) VALUES ('2018-01-01', (select cust_no from Customer where name = 'Nunes'));
insert into "order" (date, cust_no) VALUES ('2019-01-01', (select cust_no from Customer where name = 'Costa'));
insert into "order" (date, cust_no) VALUES ('2014-01-01', (select cust_no from Customer where name = 'Costa'));
insert into "order" (date, cust_no) VALUES ('2023-01-02', (select cust_no from Customer where name = 'Costa'));
insert into "order" (date, cust_no) VALUES ('2023-02-02', (select cust_no from Customer where name = 'Nunes'));
insert into "order" (date, cust_no) VALUES ('2023-01-03', (select cust_no from Customer where name = 'Nunes'));

insert into Sale (order_no) VALUES ((select order_no from "order" where date = '2017-01-01'));
insert into Sale (order_no) VALUES ((select order_no from "order" where date = '2018-01-01'));

insert into pay (order_no, cust_no) VALUES ((select order_no from "order" where date = '2017-01-01'), (select cust_no from Customer where name = 'Belchior'));
insert into pay (order_no, cust_no) VALUES ((select order_no from "order" where date = '2018-01-01'), (select cust_no from Customer where name = 'Nunes'));

insert into Employee (ssn, TIN, bdate, name) VALUES ('546654654', '123123123', '2002-04-10', 'Pedrinho');
insert into Employee (ssn, TIN, bdate, name) VALUES ('546654655', '123123124', '2002-02-14', 'Gui');
insert into Employee (ssn, TIN, bdate, name) VALUES ('546654656', '123123125', '2002-01-01', 'Luana');

insert into process (ssn, order_no) VALUES ((select ssn from Employee where name = 'Pedrinho'), (select order_no from "order" where date = '2017-01-01'));
insert into process (ssn, order_no) VALUES ((select ssn from Employee where name = 'Luana'), (select order_no from "order" where date = '2023-01-02'));
insert into process (ssn, order_no) VALUES ((select ssn from Employee where name = 'Gui'), (select order_no from "order" where date = '2019-01-01'));
insert into process (ssn, order_no) VALUES ((select ssn from Employee where name = 'Gui'), (select order_no from "order" where date = '2023-01-03'));
insert into process (ssn, order_no) VALUES ((select ssn from Employee where name = 'Pedrinho'), (select order_no from "order" where date = '2014-01-01'));

insert into Department (name) VALUES ('Sales');
insert into Department (name) VALUES ('Marketing');
insert into Department (name) VALUES ('Production');

insert into Workplace (address, lat, long) VALUES ('Rua das flores', '123', '456');
insert into Workplace (address, lat, long) VALUES ('Rua da Maria', '789', '1010');
insert into Workplace (address, lat, long) VALUES ('Rua da Lua', '789', '1012');
insert into Workplace (address, lat, long) VALUES ('Rua do Sol', '789', '1011');

insert into Office (address) VALUES ('Rua da Lua');
insert into Office (address) VALUES ('Rua do Sol');

insert into Warehouse (address) VALUES ('Rua das flores');
insert into Warehouse (address) VALUES ('Rua da Maria');


insert into works (ssn, name, address) VALUES ((select ssn from Employee where name = 'Pedrinho'), (select name from Department where name = 'Sales'), (select address from Office where address = 'Rua da Lua'));
insert into works (ssn, name, address) VALUES ((select ssn from Employee where name = 'Luana'), (select name from Department where name = 'Marketing'), (select address from Warehouse where address = 'Rua das flores'));
insert into works (ssn, name, address) VALUES ((select ssn from Employee where name = 'Gui'), (select name from Department where name = 'Production'), (select address from Warehouse where address = 'Rua das flores'));
insert into works (ssn, name, address) VALUES ((select ssn from Employee where name = 'Gui'), (select name from Department where name = 'Production'), (select address from Office where address = 'Rua do Sol'));

insert into Product (name, description, price) VALUES ('Gaming Chair', 'Chair made with love and kindness', 5.35);
insert into Product (name, description, price) VALUES ('Cake', 'Cake made by our amazing chef Luana', 10.35);
insert into Product (name, description, price) VALUES ('TV', 'LG TV 4K', 500.35);
insert into Product (name, description, price) VALUES ('Table', 'Table made with paus and cola', 50.35);

insert into EAN_Product (sku, ean) VALUES ((select sku from Product where name = 'Gaming Chair'), '1234567891234');
insert into EAN_Product (sku, ean) VALUES ((select sku from Product where name = 'Cake'), '1234567891235');
insert into EAN_Product (sku, ean) VALUES ((select sku from Product where name = 'TV'), '1234567891236');

insert into contains (sku, order_no, quantity) VALUES ((select sku from Product where name = 'Gaming Chair'), (select order_no from "order" where date = '2017-01-01'), 2);
insert into contains (sku, order_no, quantity) VALUES ((select sku from Product where name = 'Cake'), (select order_no from "order" where date = '2018-01-01'), 10);
insert into contains (sku, order_no, quantity) VALUES ((select sku from Product where name = 'TV'), (select order_no from "order" where date = '2019-01-01'), 3);
insert into contains (sku, order_no, quantity) VALUES ((select sku from Product where name = 'TV'), (select order_no from "order" where date = '2023-01-02'), 14);
insert into contains (sku, order_no, quantity) VALUES ((select sku from Product where name = 'TV'), (select order_no from "order" where date = '2023-01-03'), 3);

insert into Supplier (TIN, name, address) VALUES ('123456789', 'Goncalo', 'Rua da IKEA');
insert into Supplier (TIN, name, address) VALUES ('123456788', 'Rafael', 'Rua da LG');
insert into Supplier (TIN, name, address) VALUES ('123456787', 'Luana', 'Rua da Samsung');
insert into Supplier (TIN, name, address) VALUES ('123456786', 'Ricky', 'Rua da Apple');

insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Goncalo'), (select sku from Product where name = 'Gaming Chair'));
insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Luana'), (select sku from Product where name = 'Cake'));
insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Rafael'), (select sku from Product where name = 'TV'));
insert into supply_contract (TIN, sku) VALUES ((select TIN from Supplier where name = 'Ricky'), (select sku from Product where name = 'Table'));

insert into delivery (address, TIN) VALUES ((select address from Workplace where address = 'Rua das flores'), (select TIN from Supplier where name = 'Goncalo'));
insert into delivery (address, TIN) VALUES ((select address from Workplace where address = 'Rua da Maria'), (select TIN from Supplier where name = 'Luana'));
insert into delivery (address, TIN) VALUES ((select address from Workplace where address = 'Rua da Lua'), (select TIN from Supplier where name = 'Rafael'));
insert into delivery (address, TIN) VALUES ((select address from Workplace where address = 'Rua do Sol'), (select TIN from Supplier where name = 'Ricky'));
