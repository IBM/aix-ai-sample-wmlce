create schema if not exists testcredit;

set schema testcredit;

DROP TABLE customers;
DROP TABLE manufacturers;
DROP TABLE merchants;
DROP TABLE products;
DROP TABLE orders;
DROP TABLE lineitem;
DROP TABLE merchant_promotion;
DROP TABLE manufacturer_promotion;

CREATE TABLE customers (
  id BIGINT ,
  name VARCHAR(30) ,
  balance_owed FLOAT ,
  risk_rating SMALLINT ,
  gender CHAR(1) ,
  age SMALLINT ,
  marital_status CHAR(1) ,
  income_band VARCHAR(100) ,
  zipcode INT
) DISTRIBUTE BY HASH( id ) ORGANIZE BY ROW IN "USERSPACE1";

CREATE TABLE manufacturers (
  id BIGINT,
  name VARCHAR(30) ,
  category_id SMALLINT
) DISTRIBUTE BY HASH( id ) IN "USERSPACE1";

CREATE TABLE merchants (
  id BIGINT,
  type_id SMALLINT ,
  category_id SMALLINT ,
  zipcode INT ,
  risk_rating SMALLINT
) DISTRIBUTE BY HASH( id ) IN "USERSPACE1";

CREATE TABLE products (
  id BIGINT,
  name VARCHAR(50) ,
  manufacturer_id BIGINT ,
  category_id SMALLINT ,
  size VARCHAR(10),
  retail_price FLOAT
) DISTRIBUTE BY HASH( id ) IN "USERSPACE1";

CREATE TABLE merchant_promotion (
  id BIGINT,
  merchant_id BIGINT,
  product_id BIGINT,
  discount_rate FLOAT,
  start_date TIMESTAMP,
  end_date TIMESTAMP
) DISTRIBUTE BY HASH( id ) IN "USERSPACE1";

CREATE TABLE manufacturer_promotion (
  id BIGINT,
  manufacturer_id BIGINT,
  product_id BIGINT,
  discount_rate FLOAT,
  start_date TIMESTAMP,
  end_date TIMESTAMP
) DISTRIBUTE BY HASH( id ) IN "USERSPACE1";

CREATE TABLE orders (
  id BIGINT,
  customer_id BIGINT,
  merchant_id BIGINT,
  total_amount DOUBLE,
  order_date TIMESTAMP,
  flag CHAR(1),
  description VARCHAR(1024)
) DISTRIBUTE BY HASH( id ) IN "USERSPACE1";

CREATE TABLE lineitem (
  id BIGINT,
  order_id BIGINT,
  product_id BIGINT,
  linenumber INT,
  quantity INT,
  price FLOAT,
  tax FLOAT
) DISTRIBUTE BY HASH( id ) IN "USERSPACE1";

commit;


