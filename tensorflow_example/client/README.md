Model Scoring/Inferencing from Client (eg., AIX)

Prerequisites:

 - AIX operating system should be either 7.1 or 7.2 to run this example.
 - Python version should be 3.7

REST API for inferencing can be called from AIX LPAR or any other LPAR on which data is stored. In this example, we are assuming the data is either in DB2 database or in a csv file for which we need to run predictions. The data is retrieved on AIX LPAR and sent to flask server running on Linux LPAR to obtain predictions.

new_customers.csv     - Customer data (in csv format) for predictions
insert_into_aix_db.sh - Shell script to create a DB2 database "LOANDB" and insert data in to it from new_customers.csv
flask-aix-client.py   - Python script to run predictions on data (either from DB2 or csv) using model on Linux LPAR
curlcommad            - Curl command to invoke model on Linux LPAR


