connect to retails;

set schema testcredit;

select count_big(*) from customers;
select count_big(*) from manufacturers;
select count_big(*) from manufacturer_promotion;
select count_big(*) from merchants;
select count_big(*) from merchant_promotion;
select count_big(*) from products;
select count_big(*) from lineitem;
select count_big(*) from orders;

connect reset;
connect terminate;


