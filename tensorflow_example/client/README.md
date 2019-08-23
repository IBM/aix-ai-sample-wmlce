Model Scoring/Inferencing from Client
-------------------------------------

This code has to be run from AIX LPAR.

Prerequisites:

 - AIX operating system should be either 7.1 or 7.2 to run this example.
 - Python version should be 3.7
 - IBM DB2 python module should be installed.

REST API for inferencing can be called from AIX LPAR or any other LPAR on which data is stored. In this example, we are assuming the data is either in DB2 database or in a csv file for which we need to run predictions. The data is retrieved on AIX LPAR and sent to flask server running on Linux LPAR to obtain predictions.

File Descriptions
-----------------

new_customers.csv     - Customer data (in csv format) for predictions

insert_into_aix_db.sh - Shell script to create a DB2 database "LOANDB" and insert data in to it from new_customers.csv

flask-aix-client.py   - Python script to run predictions on data (either from DB2 or csv) using model on Linux LPAR

curlcommad            - Curl command to invoke model on Linux LPAR


Inserting Data from CSV to DB2 Database
---------------------------------------

Insert data from new_customers.csv file in to db2 database:

Login as db2inst1 user

$ su – db2inst1

Insert data from new_customers.csv file in to db2 database:
 
$ ./insert_into_aix_db.sh

The records present in the file new_customer.csv will be inserted in to a new database called LOANDB in table NEW_CUSTOMERS.




Model Scoring on AIX Data with Python 
-------------------------------------


$ python3 flask-aix-client.py <-db2|-csv> <Linux LPAR Name> <Port> <Merchant_Name>
 
The above commands will run predictions on all the data (either from db2 or csv). 


Run predictions only for a merchant

$ python3 flask-aix-client.py <-db2|-csv> <Linux LPAR Name> <Port> <Merchant_Name>

For example, this command retrieves record of merchant “Gold Acoustics” from new_customer.csv and sends it for inferencing to Linux LPAR myhostname.ibm.com.

$python3 flask-aix-client.py -db2 myhostname.ibm.com 5555 “Gold Acoustics”

Output: prediction value is 0. This merchant might not default.

Model Scoring on AIX Data with Curl Command
--------------------------------------------

Replace hostname and port number before running "curlcommand". Sample data is given in the script.

$ ./curlcommand


