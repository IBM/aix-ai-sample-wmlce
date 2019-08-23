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

db2 "create db retails"
db2 connect to retails
db2 update db cfg for retails using logfilsiz 81920

db2 -tvf dbscripts/fraud_base/1_create_tbs.clp 2>&1 | tee dbscripts/fraud_base/1_create_tbs_local.out
db2 -tvf dbscripts/fraud_base/2_data_ld_dm_1node.clp 2>&1 | tee dbscripts/fraud_base/2_data_ld_dm_1node.out
db2 -tvf dbscripts/fraud_base/3_data_ld_fac_1node.clp 2>&1 | tee dbscripts/fraud_base/3_data_ld_fac_1node.out

db2 -tvf dbscripts/fraud_gentran/1_assign_risk.clp 2>&1 | tee dbscripts/fraud_gentran/1_assign_risk_local.out
db2 -tvf dbscripts/fraud_gentran/2_gen_bigtran.clp 2>&1 | tee dbscripts/fraud_gentran/2_gen_bigtran_local.out


