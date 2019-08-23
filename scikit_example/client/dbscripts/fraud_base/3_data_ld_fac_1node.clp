-- To run this script using "db2 -tvf db2vol_ld_fac_1TB.clp 2>&1 | tee db2_ld_fac_1TB.out"

connect to retails;

set schema testcredit;

LOAD FROM ./datagen/lineitem of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into lineitem;

LOAD FROM ./datagen/order of del modified by timestampformat="YYYY-MM-DD HH:MM:SS" coldel| insert into orders;

select count(*) from lineitem;
select count(*) from orders;
connect reset;
terminate;
