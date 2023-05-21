insert into Customer VALUES ('Belchior', 'belchiorlindo@gmail.com', '912345678', 'Rua do Belchior');
insert into Customer VALUES ('Nunes', 'danielnunes@gmail.com', '939393939', 'Rua do Nunes');
insert into Customer VALUES ('Costa', 'joaolscosta@gmail.com', '947854684', 'Rua das flores');

insert into Order VALUES ('2017-01-01', (select cust_no from Customer where name = 'Belchior'));
insert into Order VALUES ('2018-01-01', (select cust_no from Customer where name = 'Nunes'));
insert into Order VALUES ('2019-01-01', (select cust_no from Customer where name = 'Costa'));
insert into Order VALUES ('2014-01-01', (select cust_no from Customer where name = 'Costa'));

insert into Sale VALUES ((select order_no from Order where date = '2017-01-01'));
insert into Sale VALUES ((select order_no from Order where date = '2018-01-01'));

insert into pay VALUES ((select order_no from Order where date = '2017-01-01'), (select cust_no from Customer where name = 'Belchior'));
insert into pay VALUES ((select order_no from Order where date = '2018-01-01'), (select cust_no from Customer where name = 'Nunes'));

insert into Employee VALUES ('546654654', '123123123', '2002-04-10', 'Pedrinho');
insert into Employee VALUES ('546654655', '123123124', '2002-02-14', 'Gui');
insert into Employee VALUES ('546654656', '123123125', '2002-01-01', 'Luana');

insert into process VALUES ((select ssn from Employee where name = 'Pedrinho'), (select order_no from Order where date = '2017-01-01'));
insert into process VALUES ((select ssn from Employee where name = 'Luana'), (select order_no from Order where date = '2018-01-01'));
insert into process VALUES ((select ssn from Employee where name = 'Gui'), (select order_no from Order where date = '2019-01-01'));
insert into process VALUES ((select ssn from Employee where name = 'Pedrinho'), (select order_no from Order where date = '2014-01-01'));

insert into Department VALUES ('Sales');
insert into Department VALUES ('Marketing');
insert into Department VALUES ('Production');

insert into Workplace VALUES ('Rua das flores', '123', '456');
insert into Workplace VALUES ('Rua da Maria', '789', '1012');
insert into Workplace VALUES ('Rua da Lua', '789', '1012');
insert into Workplace VALUES ('Rua da Sol', '789', '1012');

insert into Office VALUES ('Rua da Lua');
insert into Office VALUES ('Rua do Sol');

insert into Warehouse VALUES ('Rua das flores');
insert into Warehouse VALUES ('Rua da Maria');


insert into works VALUES ((select ssn from Employee where name = 'Pedrinho'), (select name from Department where name = 'Sales'), (select address from Office where address = 'Rua da Lua'));
insert into works VALUES ((select ssn from Employee where name = 'Luana'), (select name from Department where name = 'Marketing'), (select address from Warehouse where address = 'Rua das flores'));
insert into works VALUES ((select ssn from Employee where name = 'Gui'), (select name from Department where name = 'Production'), (select address from Office where address = 'Rua do Sol'));

insert into Product VALUES ('Gaming Chair', 'Chair made with love and kindness', 5.35);
insert into Product VALUES ('Cake', 'Cake made by our amazing chef Luana', 10.35);
insert into Product VALUES ('TV', 'LG TV 4K', 500.35);
insert into Product VALUES ('Table', 'Table made with paus and cola', 50.35);

insert into EAN_Product VALUES ((select sku from Product where name = 'Gaming Chair'), '1234567891234');
insert into EAN_Product VALUES ((select sku from Product where name = 'Cake'), '1234567891235');
insert into EAN_Product VALUES ((select sku from Product where name = 'TV'), '1234567891236');

insert into contains VALUES ((select sku from Product where name = 'Gaming Chair'), (select order_no from Order where date = '2017-01-01'), 2);
insert into contains VALUES ((select sku from Product where name = 'Cake'), (select order_no from Order where date = '2018-01-01'), 10);
insert into contains VALUES ((select sku from Product where name = 'TV'), (select order_no from Order where date = '2019-01-01'), 3);

insert into Supplier VALUES ('123456789', 'Goncalo', 'Rua da IKEA');
insert into Supplier VALUES ('123456788', 'Rafael', 'Rua da LG');
insert into Supplier VALUES ('123456787', 'Luana', 'Rua da Samsung');
insert into Supplier VALUES ('123456786', 'Ricky', 'Rua da Apple');

insert into supply_contract VALUES ((select TIN from Supplier where name = 'Goncalo'), (select sku from Product where name = 'Gaming Chair'));
insert into supply_contract VALUES ((select TIN from Supplier where name = 'Luana'), (select sku from Product where name = 'Cake'));
insert into supply_contract VALUES ((select TIN from Supplier where name = 'Rafael'), (select sku from Product where name = 'TV'));
insert into supply_contract VALUES ((select TIN from Supplier where name = 'Ricky'), (select sku from Product where name = 'Table'));

insert into delivery VALUES ((select address from Warehouse where address = 'Rua das flores'), (select TIN from Supplier where name = 'Goncalo'));
insert into delivery VALUES ((select address from Warehouse where address = 'Rua da Maria'), (select TIN from Supplier where name = 'Luana'));
insert into delivery VALUES ((select address from Warehouse where address = 'Rua da Lua'), (select TIN from Supplier where name = 'Rafael'));
insert into delivery VALUES ((select address from Warehouse where address = 'Rua da Sol'), (select TIN from Supplier where name = 'Ricky'));