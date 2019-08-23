set schema testcredit;

DROP TABLE transaction;

CREATE TABLE transaction (
                         TRANS_ID         BIGINT ,
                         PRODUCT_ID       BIGINT,
                         LINE_NUMBER      INTEGER,
                         QUANTITY         INTEGER,
                         PRICE            DOUBLE,
                         TAX              DOUBLE,
                         CUSTOMER_ID      BIGINT,
                         MFR_ID           BIGINT,
                         PROD_NAME        VARCHAR(50),
                         PROD_CATEGORY    SMALLINT,
                         PROD_SIZE        VARCHAR(10),
                         RETAIL_PRICE     DOUBLE,
                         RISK_RATING      DOUBLE,
                         INCOME_BAND      VARCHAR(100),
                         CREDIT_LIMIT     INTEGER,
                         FLAG             CHAR(1),
                         TRANS_TIMESTAMP  TIMESTAMP,
                         YEAR             INTEGER,
                         MONTH            INTEGER,
                         DAY              INTEGER
) DISTRIBUTE BY HASH(TRANS_ID) ORGANIZE BY ROW IN "USERSPACE1";

commit;

EXPORT TO ./dbscripts/fraud_gentran/transaction.csv OF DEL 
SELECT
        l.order_id,
        l.product_id,
        l.linenumber,
        l.quantity,
        l.price,
        l.tax,
        t.customer_id,
        t.merchant_id,
        p.name,
        p.category_id,
        p.size,
        p.retail_price,
        c.risk_rating,
        c.income_band,
        case when c.income_band = '150000-500000$' then 15000
             when c.income_band =  '50000-150000$' then 5000
             when c.income_band =  '10000-50000$' then 2500
             when c.income_band =  'over 500000$' then 30000
             when c.income_band = 'under 20000$' then 1000
        end,
        t.flag,
        t.order_date,
        YEAR(t.order_date),
        MONTH(t.order_date),
        DAY(t.order_date)
  FROM
        lineitem l,
        trans_sm t,
        products p,
        customers c
  WHERE
        l.order_id = t.id and
        l.product_id = p.id and
        c.id = t.customer_id 
        and
        MONTH(t.order_date) = 1; 
--		and DAY(t.order_date) = 2;

load from ./dbscripts/fraud_gentran/transaction.csv of del 
    messages ./dbscripts/fraud_gentran/tran_load.out 
    insert into transaction (  
         trans_id,
         product_id,
         LINE_NUMBER,
         QUANTITY,
         PRICE,
         TAX,
         customer_id,
         mfr_id,
         PROD_NAME,
         PROD_CATEGORY,
         PROD_SIZE,
         RETAIL_PRICE,
         RISK_RATING,
         INCOME_BAND,
         CREDIT_LIMIT,
         FLAG,
         TRANS_TIMESTAMP,
         YEAR,
         MONTH,
         DAY
    )
    nonrecoverable;

commit;

grant connect, dataaccess on database to retails;

