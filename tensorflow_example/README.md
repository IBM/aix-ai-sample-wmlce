Tensorflow based Model
----------------------

Usecase:
--------

This use case on retaining Merchants that are using company network for credit card processing.  A client approved many low value merchant accounts without much scrutiny. Many of those merchant accounts resulted in default.   Those merchant accounts were focusing on the following joint programs cars, furniture, electronics, continuing education, etc.  The client thinks that they should have put more of an emphasis on their applicant screening process.

This example has two folders:
 - client - code to run from client system (ex AIX). This has code which reads data from DB2 and sent it to server for inferencing.
 - server - code to run from server system (ex LINUX). This has code for model training, deployment and exporting the model via REST APIs



