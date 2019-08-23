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
from Predictors import RiskPredictor

app = Flask(__name__)
api = Api(app)

# Create predictor
predictor = RiskPredictor()

class User(Resource):
    def get(self):
        if predictor.status == predictor.PRED_STATUS['READY_FOR_WORK']:
            return {'status': 'READY'}, 200

        if predictor.status == predictor.PRED_STATUS['BUSY']:
            return {'status': 'BUSY'}, 503

        return {'status': 'Initializing' }, 200


    def post(self):
        if predictor.status == predictor.PRED_STATUS['BUSY']:
            return {'status': 'BUSY'}, 503

        predictor.status = predictor.PRED_STATUS['BUSY']

        print(request)
        parser = reqparse.RequestParser()
        parser.add_argument("TRANS_ID")
        parser.add_argument("PRODUCT_ID")
        parser.add_argument("LINE_NUMBER")
        parser.add_argument("QUANTITY")
        parser.add_argument("PRICE")
        parser.add_argument("TAX")
        parser.add_argument("CUSTOMER_ID")
        parser.add_argument("MFR_ID")
        parser.add_argument("PROD_NAME")
        parser.add_argument("PROD_CATEGORY")
        parser.add_argument("PROD_SIZE")
        parser.add_argument("RETAIL_PRICE")
        parser.add_argument("RISK_RATING")
        parser.add_argument("INCOME_BAND")
        parser.add_argument("CREDIT_LIMIT")

        args = parser.parse_args()
        arg_len = len(args)

        if (arg_len > 0):
            row = [ args["TRANS_ID"], args["PRODUCT_ID"], args["LINE_NUMBER"], args["QUANTITY"], args["PRICE"], args["TAX"], args["CUSTOMER_ID"], args["MFR_ID"], args["PROD_NAME"], args["PROD_CATEGORY"], args["PROD_SIZE"], args["RETAIL_PRICE"], args["RISK_RATING"], args["INCOME_BAND"], args["CREDIT_LIMIT"] ]

            print(row)
            prob = predictor.predict(row)

        # In case that an empty row is given, just return the value 0 indicating that has
        # zero chance to be a fraud transaction.  We don't want to return error to the
        # caller (e.g. ZINCserver) to avoid error handling from higher levels.
        else:
            prob = 0

        print(prob)            
        predictor.status = predictor.PRED_STATUS['READY_FOR_WORK']

        return {"Prob": str(prob)}, 201


    def put(self, I1):
        return {"Error": "Method not supported"}, 404

    def delete(self, I1):
        return {"Error": "Method not supported"}, 404
     
 
api.add_resource(User, "/user")

app.run(debug=True, host="0.0.0.0", port=5001 )

