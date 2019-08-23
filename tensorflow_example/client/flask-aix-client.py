#!/usr/bin/python3

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

#This python script has to be run from a client LPAR (Ex: AIX system)
#This script reads data either from DB2 database or csv file and sends data to server for inferencing

import requests
import time

global server_name, port_number

def predict_results(features):
    global model, graph
    with graph.as_default():
            result = model.predict_classes(features)
    return result

def predict_using_rest_api(colheaders, features):
    global server_name, port_number
    server_string = "http://" + server_name + ":" + port_number + "/predict"
    url = server_string
    #print ("url is " + url)
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    data = [ { 'headers': colheaders, 'features': features }]
    prediction = requests.post(url, json=data, headers=headers).json()
    pred=prediction[0]['prediction']
    extract_pred=pred[0]
    final_prediction=extract_pred[0]
    #print "final prediction is " + str(final_prediction)
    #prediction = np.squeeze(prediction[0]['prediction'])
    return final_prediction


def main():
	global server_name, port_number
	import sys
	if len(sys.argv)!= 4 and len(sys.argv)!= 5 :
		print_usage()
		sys.exit(1)
	option = sys.argv[1]
	server_name=sys.argv[2]
	port_number=sys.argv[3]

	if option!="-db2" and option!="-csv":
		print("Error: Invalid option " + option +". Please provide either -db2 or -csv as input")
		print_usage()
		sys.exit(1)

	if  not port_number.isdigit():
		print("Error: Invalid Port Number")
		print_usage()
		sys.exit(1)

	if (len(sys.argv) == 5):
		merchant=sys.argv[4]
	else:
		merchant=''
	headers = ['ACCT_STATUS_K_USD', 'CONTRACT_DURATION_MONTH', 'HISTORY','CREDIT_PROGRAM', 'AMOUNT_K_USD', 'ACCOUNT_TYPE', 'ACCT_AGE', 'STATE','IS_URBAN', 'IS_XBORDER', 'SELF_REPORTED_ASMT', 'CO_APPLICANT', 'GUARANTOR', 'PRESENT_RESIDENT', 'OWN_REAL_ESTATE', 'PROP_UNKN', 'ESTABLISHED_MONTH', 'OTHER_INSTALL_PLAN', 'RENT', 'OWN_RESIDENCE', 'NUMBER_CREDITS', 'RFM_SCORE', 'BRANCHES', 'TELEPHONE', 'SHIP_INTERNATIONAL']
	if option=="-db2":
		predict_fromdb2(headers,merchant)
	if option=="-csv":
		predict_fromcsv(headers,merchant)

def predict_fromcsv(headers,merchant):
	import ast
	merchant_present=0
	filename="new_customers.csv"
	file1 = open(filename,'r')
	lines=file1.read().splitlines()
	#remove column names
	lines_data=lines[1:]
	#length=len(lines)
	if not merchant:
		merchant_present=1
		for row in lines_data:
			#convert string to dictionary
			row=ast.literal_eval(row)
			merchant_name=row[0]
			#after removing merchant name
			final_row=row[1:]
			print ("Data sent to server:")
			print ("====================")
			print (row)
			p = predict_using_rest_api(headers,list(final_row))
			if p==0:
				print("Prediction value is 0. This account might not default\n")
			else:
				print("Prediction value is 1. This account might default\n")
	else:
		for row in lines_data:
			row=ast.literal_eval(row)
			merchant_name=row[0]
			final_row=row[1:]
			if merchant==merchant_name:
				print ("Data sent to server:")
				print ("====================")
				print (row)
				p = predict_using_rest_api(headers,list(final_row))
				merchant_present=1
				if p==0:
					print("Prediction value is 0. This account might not default\n")
				else:
					print("Prediction value is 1. This account might default\n")
						
	if merchant_present == 0:
		print("No such merchant with name " + merchant)


def predict_fromdb2(headers,merchant):
	import ibm_db_dbi as db
	import sys
	if not merchant:
		query = 'SELECT * FROM NEW_CUSTOMERS'
	else:
		query = 'SELECT * FROM NEW_CUSTOMERS where merchant=\'' + merchant +'\''
	#print (query)
	conn = db.connect("DATABASE=LOANDB;UID=db2inst1;PWD=db2inst1")
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	if len(rows)== 0:
		print("No matching data found in database")
		sys.exit(1)
	#data = datas[1:]
	#print data
	i = 1
	for row in rows:
		#skip merchant name
		data = row[1:]
		print ("Processing record " + str(i))
		i = i + 1
		#print (list(data))
		#print headers
		p = predict_using_rest_api(headers,list(data))

		print ("Data sent to server:")
		print ("====================")
		print (row)
		print ("------------------------------------------------------------------------")
		if p==0:
			print("Prediction value is 0. This account might not default\n")
		else:
			print("Prediction value is 1. This account might default\n")

def print_usage():
		print ("Usage: python flask-aix-client.py <-db2|-csv> <Linux LPAR> <Port Number> [merchant_name]")
		print ("<-db2>: if your data is in db2 database")
		print ("<-csv>: if your data is in csv format")
		print ("<Server Name>: Name or IP address of Linux LPAR where flask server is running")
		print ("<Port Number>: Port number on which server is running")
		print ("[merchant_name]: Optional argument. Input merchant name.")

if __name__ == '__main__':
	main()
