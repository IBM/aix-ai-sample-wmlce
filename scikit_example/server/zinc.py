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

import os, ibm_db, json, requests, operator
from operator import itemgetter
from bson.json_util import dumps

import time
from functools import wraps

PROF_DATA = {}
PROF_LOGGING = "N"

def profile(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        if PROF_LOGGING == "N":
            return fn(*args, **kwargs)
        else:
            start_time = time.perf_counter()

            ret = fn(*args, **kwargs)

            elapsed_time = time.perf_counter() - start_time

            if fn.__name__ not in PROF_DATA:
                PROF_DATA[fn.__name__] = [0, []]
            PROF_DATA[fn.__name__][0] += 1
            PROF_DATA[fn.__name__][1].append(elapsed_time)

            return ret

    return with_profiling

def print_prof_data( app ):
    for fname, data in PROF_DATA.items():
        max_time = max(data[1])
        avg_time = sum(data[1]) / len(data[1])
        app.logger.info( 'Function %s called %d times. ' %(fname, data[0]) )
        app.logger.info( 'Execution time max: %.3f, average: %.3f' %(max_time, avg_time) )

def clear_prof_data():
    global PROF_DATA
    PROF_DATA = {}

def log_off():
    global PROF_LOGGING
    PROF_LOGGING = "N"

def log_on():
    global PROF_LOGGING
    PROF_LOGGING = "Y"

class ZINCServer:
    """ Zeppelin INferencing Collateral server

        Args:
            just takes one argument - the USER ID
            to look for. 

        Dependencies:

            DB2 server
                defined via the environment variable DB2_DSN
                    - value such as:
                      DB2_DSN='DRIVER={IBM DB2 ODBC DRIVER};DATABASE=test1;HOSTNAME=<hostname>;PORT=50000;PROTOCOL=TCPIP;UID=test1;PWD=test1;'

            CTR server
                defined via the environment variable CTR_URI
                    - values such as:
                       CTR_URI=http://<HOST IP>:5001/user
    """
  
    # Status definitions
    ZINC_STATUS = {'NOT_INITIALIZED':0, 'READY_FOR_WORK':1, 'BUSY':2, 'ERROR':3}

    # Use status field to block pod from being used when not ready or busy 
    status = ZINC_STATUS['NOT_INITIALIZED'] 

    @profile
    def __init__(self, app):
        """
        Description
            Initializes the ZINC server object.  Establishes connection to
            DB2.


        Arguments
            Requires the app from Flask.
            The database connection information is passed in via environment
            variables.


        Returns:
            None.  However, the database settings should already be set here, 
            as well as any other resources required later on.

        TODO: Add in error checking for the environment variables.

        """
        self.status = self.ZINC_STATUS['NOT_INITIALIZED']
        self.DB2_DSN = os.environ['DB2_DSN']
        self.CTR_URI=os.environ['CTR_URI']

        self.db2_connection = ibm_db.connect( self.DB2_DSN, '', '' )
        self.db2_sql = "select trans_id, product_id, line_number, quantity, price, tax, customer_id, mfr_id, prod_name, prod_category, prod_size, retail_price, risk_rating, income_band, credit_limit, flag FROM testcredit.transaction where trans_id = ? limit 100"

        self.db2_stmt = ibm_db.prepare( self.db2_connection, self.db2_sql )
        self.status = self.ZINC_STATUS['READY_FOR_WORK']

    @profile
    def trans_db(self, id):
        """
        Description
            Fetches the user database records from the DB2 database. Requires
            that the database connection already be set up.

        Arguments
            user - the user ID that we will query the DB2 database.  

        Returns:
            A list of dictionaries, with a maximum of 100 rows.

        """

        ibm_db.bind_param( self.db2_stmt, 1, id )
        ibm_db.execute( self.db2_stmt )
        dictResult = ibm_db.fetch_assoc( self.db2_stmt )

        listDicts = []
        while dictResult != False:
            listDicts.append( dictResult )
            dictResult = ibm_db.fetch_assoc( self.db2_stmt )

        return listDicts


    @profile
    def risk_score(self, trans_id):
        """
        Description
            When given a trans id, will query the DB2 database 

        Arguments
            transaction id.

        Returns:
	    predicted risk score.

        """
        if ( self.status != self.ZINC_STATUS['READY_FOR_WORK'] ) :
             output = "Error! POD is not ready for work..."
             return output

        self.status = self.ZINC_STATUS['BUSY']
        trans_id = trans_id.strip('\"')
        trans_id = trans_id.rstrip()
        output = ""
        user_db_results = self.trans_db( trans_id )

        # Error checking for NULL result
        num_items = len( user_db_results )
        if (num_items == 0) :
            output = "Error! Cannot find transaction record for [" + trans_id + "]!"
            self.status = self.ZINC_STATUS['READY_FOR_WORK']
            return output

        listTrainResults = []
        count = 0
        while count < num_items:
            user_db_result = user_db_results[count]

            # Call the CTR predictor.  We call once per row
            # and then append the results to another list.

            # We will retry 10 times for Predictor busy cases.  If we fail for all 10 trys
            # The value 0 is used as the inferencing value from the predictor
            listTempResult = self.call_ctr( user_db_result )

            listTrainResults.append( listTempResult )

            count = count + 1

        maxScore = max(listTrainResults)
        self.status = self.ZINC_STATUS['READY_FOR_WORK'] 
        return dumps( maxScore )

    @profile
    def call_ctr( self, payload ):
        """
        Description
            Call the Click Through Rate predictor program.  The URI for this
            is passed in via an environment variable.


        Arguments
            A dictionary with all the values needed by the CTR predictor.


        Returns:
            the output from the CTR program. 

        """

        i = 0
        while (i < 10):
            response = requests.post( self.CTR_URI, data=payload )
            if response.status_code < 400:
                break
            else:
                print("zinc server received %d from predictor, retry %d" % (response.status_code, i))
                i = i + 1

        prob = 0
        if response:
            result = response.json()
            prob = json.loads( result["Prob"] )

        return prob


