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

# This is a helper file for train.py to read the data from csv file and do data transformation
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.externals import joblib

colTransform= { 'ACCT_STATUS_K_USD': 1, 'CONTRACT_DURATION_MONTH': 0, 'HISTORY': 1,
		'CREDIT_PROGRAM': 1, 'AMOUNT_K_USD': 0, 'ACCOUNT_TYPE': 1, 
		'ACCT_AGE': 1, 'STATE': 1, 'IS_URBAN': 1, 'IS_XBORDER': 1,
		'SELF_REPORTED_ASMT': 1, 'CO_APPLICANT': 1, 'GUARANTOR': 1, 
		'PRESENT_RESIDENT': 1, 'OWN_REAL_ESTATE': 1, 'PROP_UNKN': 1, 
		'ESTABLISHED_MONTH': 0, 'OTHER_INSTALL_PLAN': 1, 'RENT': 1, 
		'OWN_RESIDENCE': 1, 'NUMBER_CREDITS': 0, 'RFM_SCORE': 0, 'BRANCHES': 0, 
		'TELEPHONE': 1, 'SHIP_INTERNATIONAL': 1, 'IS_DEFAULT': 1 }

all_columns = ['ACCT_STATUS_K_USD', 'CONTRACT_DURATION_MONTH', 'HISTORY', 'CREDIT_PROGRAM', 
		'AMOUNT_K_USD', 'ACCOUNT_TYPE', 'ACCT_AGE', 'STATE', 'IS_URBAN', 'IS_XBORDER', 
		'SELF_REPORTED_ASMT', 'CO_APPLICANT', 'GUARANTOR', 'PRESENT_RESIDENT', 
		'OWN_REAL_ESTATE', 'PROP_UNKN', 'ESTABLISHED_MONTH', 'OTHER_INSTALL_PLAN', 'RENT',
               'OWN_RESIDENCE', 'NUMBER_CREDITS', 'RFM_SCORE', 'BRANCHES', 'TELEPHONE', 
		'SHIP_INTERNATIONAL', 'IS_DEFAULT']

def extract_features(features_raw, le=None, mm_scalar=None):
	#May or may not have 'IS_DEFAULT'
	cols = all_columns if (features_raw.shape[1] == len(all_columns)) else all_columns[0:-1]	

	df = pd.DataFrame(data=features_raw, columns=cols)

	if le == None:
		le = {}
		for col in cols:
			if colTransform[col] == 1:
				tle = LabelEncoder()
				tle.fit(df[col])
				le[col] = tle
				df[col] = le[col].transform(df[col])
			else:
				print ("Skipping.. ", col)

	if 'IS_DEFAULT' in df.columns:
		Y = np.float32(df.IS_DEFAULT)
		Y = np.reshape(Y, (len(Y), 1))
		df = df.drop('IS_DEFAULT',axis=1)
	else:
		Y = np.full((len(df),1),-1)


	if mm_scalar == None:
		mm_scalar = MinMaxScaler()
		mm_scalar.fit(df)

	features = mm_scalar.transform(df)

	return features,Y,le,mm_scalar

def read_csv_file(fname, le=None, mm_scalar=None):
	df = pd.read_csv(fname)
	df = df.drop('MERCHANT',axis=1)

	features_raw = df.values
	features,Y,le,mm_scalar = extract_features(features_raw,le,mm_scalar)
	return (features,Y,le,mm_scalar)
	

def read_customer_history():
	return read_csv_file("./cust_history.csv")

def read_customer_data(fname = "./new_customers.csv"):
	df = pd.read_csv(fname)
	
	if 'MERCHANT' in df.columns:
		df = df.drop('MERCHANT', axis=1)

	if 'IS_DEFAULT' in df.columns:
		Y = df['IS_DEFAULT']
		df = df.drop('IS_DEFAULT',axis=1)
	else:
		Y=np.full((len(df), 1), -1)

	return (df, Y)
