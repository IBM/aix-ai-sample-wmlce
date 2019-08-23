#!/bin/sh

##############################################################################
# (c)Copyright 2019 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

#Shell script to create a database and insert records from NEW_CUSTOMERS.csv in to database named LOANDB"

set -x
db2 "create database loandb"
db2 connect to loandb
db2 "CREATE TABLE new_customers (MERCHANT VARCHAR(128), ACCT_STATUS_K_USD VARCHAR(64), CONTRACT_DURATION_MONTH INT, HISTORY VARCHAR(128), CREDIT_PROGRAM VARCHAR(64), AMOUNT_K_USD INT, ACCOUNT_TYPE VARCHAR(64), ACCT_AGE VARCHAR(64), STATE CHAR(2), IS_URBAN VARCHAR(3), IS_XBORDER VARCHAR(3), SELF_REPORTED_ASMT VARCHAR(3), CO_APPLICANT VARCHAR(3), GUARANTOR VARCHAR(3), PRESENT_RESIDENT VARCHAR(32), OWN_REAL_ESTATE  VARCHAR(3), PROP_UNKN VARCHAR(3), ESTABLISHED_MONTH INT, OTHER_INSTALL_PLAN VARCHAR(3), RENT VARCHAR(3), OWN_RESIDENCE VARCHAR(3), NUMBER_CREDITS   INT, RFM_SCORE INT, BRANCHES INT, TELEPHONE VARCHAR(3), SHIP_INTERNATIONAL VARCHAR(3))";
db2 "List Tables"
db2 "select * from NEW_CUSTOMERS"
db2 import from NEW_CUSTOMERS.csv of del replace into NEW_CUSTOMERS
db2 "select * from NEW_CUSTOMERS" limit 2

