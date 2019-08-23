-- To run this script using "db2 -tvf db2vol_ld_dm_1TB.clp 2>&1 | tee db2_ld_dm_1TB.out"

connect to retails;

set schema testcredit;

LOAD FROM ./datagen/customer of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into customers;

LOAD FROM ./datagen/manufacturer of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into manufacturers;

LOAD FROM ./datagen/manufacturer_promotion of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into manufacturer_promotion;

LOAD FROM ./datagen/merchant of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into merchants;

LOAD FROM ./datagen/merchant_promotion of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into merchant_promotion;

LOAD FROM ./datagen/product of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into products;

select count(*) from customers;
select count(*) from manufacturers;
select count(*) from manufacturer_promotion;
select count(*) from merchants;
select count(*) from merchant_promotion;
select count(*) from products;

connect reset;
terminate;

