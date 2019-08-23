#!/usr/bin/env python
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

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from zinc import ZINCServer, profile, print_prof_data, clear_prof_data, log_on, log_off

from bson.json_util import dumps
import json

app = Flask(__name__)
api = Api( app )

zincserver = ZINCServer(app)

class ZincDriver(Resource):
    """
    Description:
        This is the main driver for the ZINC service.  
        Input is only accepted via a POST call, and takes
        one parameter: UerID.

    """

    def get( self ):
        if zincserver.status == zincserver.ZINC_STATUS['READY_FOR_WORK']:
            return {'status': 'READY'}, 200

        if zincserver.status == zincserver.ZINC_STATUS['BUSY']:
            return {'status': 'BUSY'}, 503

        return {'status': 'Initializing' }, 200
        

    def post( self ):

        if zincserver.status == zincserver.ZINC_STATUS['BUSY']:
            return {'status': 'BUSY'}, 503

        print( request )
        results = []
        parser = reqparse.RequestParser()
        parser.add_argument( "TransID" )
        parser.add_argument( "Stats" )
        parser.add_argument( "ResetStats" )
        parser.add_argument( "Logging" )

        args = parser.parse_args()
        arg_len = len(args)

        if args['ResetStats'] == "Y":
            clear_prof_data()
            results.append( {"ResetStats": "True" } )

        if args['Logging'] == "Y":
            log_on()
            results.append( {"Logging": "ON"} )

        if args['Logging'] == "N":
            log_off()
            results.append( {"Logging": "Off" } )


        trans_id = args["TransID"]
        if trans_id is not None:
            trans_id.strip('\"')
            results = zincserver.risk_score( trans_id )

        if args["Stats"] == "Y":
            print_prof_data( app )

        return results, 201

    def put(self, I1):
        return "Method not supported", 404

    def delete(self, I1):
        return "Method not supported", 404

api.add_resource( ZincDriver, "/risk_score")


# Start the flask application.  The default port is 5000.  To specify
# a different port, add another parameter, "port=xxxx" to the
# app.run command arguments.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
