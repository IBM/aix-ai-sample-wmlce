set schema testcredit;

drop table trans_sm;

CREATE TABLE trans_sm (
 id BIGINT ,
 customer_id BIGINT,
 merchant_id BIGINT,
 order_date TIMESTAMP,
 flag CHAR(1),
 description VARCHAR(1024),
 total_amount double
) DISTRIBUTE BY HASH(id) ORGANIZE BY ROW IN "USERSPACE1";

commit;

EXPORT TO ./dbscripts/fraud_gentran/tran_pre.csv OF DEL 
SELECT orders.id, orders.customer_id, orders.merchant_id, orders.order_date, orders.flag, orders.description, sum(l.quantity*l.price*(1+l.tax)) AS total_amount FROM lineitem l, orders 
WHERE orders.id = l.order_id  
GROUP BY orders.id,customer_id,merchant_id,order_date,flag,description;

load from ./dbscripts/fraud_gentran/tran_pre.csv of del 
 messages ./dbscripts/fraud_gentran/load_tran.out 
insert into trans_sm nonrecoverable;

commit;

drop table temprisk;

create table temprisk
( risk_rating smallint,
  ID          bigint);

insert into temprisk (risk_rating, id)
  select    count(case when (m.category_id = 6 and t.total_amount > 300) or
                                (m.category_id = 11 and t.total_amount > 400) or
                                (m.category_id = 21 and t.total_amount > 100) then 1 else null end)*100/count(*) risk,
                t.customer_id t_id
      from trans_sm t, merchants m
      where t.merchant_id = m.id
      group by t.customer_id
;

commit;

update customers c1
  set c1.risk_rating = 
  (  select t.risk_rating 
     from temprisk t
     where c1.id = t.id
  );

commit;

update trans_sm
set flag = 'R'
where id in (
select t.id
from trans_sm t, (select id, risk_rating,
       case when income_band = '150000-500000$' then 15000
            when income_band =  '50000-150000$' then 5000
            when income_band =  '10000-50000$' then 2500
            when income_band =  'over 500000$' then 30000
            when income_band = 'under 20000$' then 1000
        end as credit_limit
    from customers) as c
where t.customer_id = c.id
  and (
       (c.risk_rating < 30 and t.total_amount/c.credit_limit*100 > 50) or
       (c.risk_rating > 50 and t.total_amount/c.credit_limit*100 > 10) or
       (c.risk_rating between 30 and 50 and t.total_amount/c.credit_limit*100 > 25)
  )
);

commit;      
