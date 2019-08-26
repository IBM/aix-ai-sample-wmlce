**Scikit-Based Model**

Usecase:

This usecase shows an example where the customer behavior and purchase history is used to identify the risk score for each of the retail transaction. This risk score is used to decide if a transaction is safe to be committed. 

The model can be deployed on a Linux LPAR that has WML-CE installed and the model is served using REST APIs. It can be accessed for inferencing either from AIX before committing a transaction or from a “Point of Sale” system that is updating the DB2 for the retail transactions.

This example has two folders:

    client - code to run from client system (ex AIX). This has code which creates db2 database with data.
    server - code to run from server system (ex LINUX). This has code for model training, deployment and exporting the model via REST APIs
