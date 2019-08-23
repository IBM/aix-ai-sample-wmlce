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

#This script has to be run on RHEL POWER VM Linux Lpar
#This script loads the model and exports REST API using flask for inferencing

from flask import request,jsonify,Flask
import numpy as np
import pandas as pd
from process_data import colTransform
import sys
global sess

def load_model():
    global sess
    import tensorflow as tf
    from tensorflow.python.keras.backend import set_session
    from sklearn.externals import joblib
    from tensorflow.python import keras as keras
    import os
    global model,le,mm_scalar, graph, sess
    sess = tf.compat.v1.Session()
    set_session(sess)
    if os.path.exists('./cc_risk_analysis_model.h5') and os.path.exists('./feature_transform_model.pkl'):
        model = keras.models.load_model('./cc_risk_analysis_model.h5')
        le,mm_scalar = joblib.load('./feature_transform_model.pkl')
    else:
        print("flask-linux-server.py Error: Model not found, please run 'python3 train.py' to generate the model")
        sys.exit(1)
    graph = tf.compat.v1.get_default_graph()

app = Flask(__name__)

def data_transform(headers, features):
    global model,le,mm_scalar, graph

    tdata = []
    for idx,col in enumerate(headers):
        if colTransform[col] == 1:
            #le_maps = dict(zip(le[col].classes_, le[col].transform(le[col].classes_)))
            #print le_maps
            tdata.append(le[col].transform([features[idx]])[0])
        else:
            tdata.append(features[idx])
    
    df = pd.DataFrame(data=[tdata], columns=headers)
    r = mm_scalar.transform(df)
    return r

def predict_results(features):
    global model, graph
    with graph.as_default():
            result = model.predict_classes(features)
    return result
            

@app.route("/predict", methods=['POST'])
def predict():
    from tensorflow.python.keras.backend import set_session
    set_session(sess)
    params = request.get_json(silent=True)
    parameters = params[0]
    headers = parameters['headers']
    features = np.array(parameters['features'])

    #print "Header" , headers
    print("Data received from client")
    print ("=========================")
    print (features)
    print ("------------------------------------------------------------------------")
    tdata = data_transform(headers, features)
    print ("Transformed Data")
    print ("================")
    a = np.array(tdata).reshape(1, 25)
    print (a)
    print ("------------------------------------------------------------------------")

    prediction = predict_results(a)
    print ("Response to client: ", prediction.tolist()[0])

    print ("")
    print ("")
    return jsonify([{'prediction':prediction.tolist()}])


def main():
    if len(sys.argv)!= 3:
        print ("Usage: python flask-linux-server.py <Linux LPAR Name> <Port Number>")
        print ("<Server Name>: Name or IP address of your Linux LPAR")
        print ("<Port Number>: Desired port number")
        sys.exit(1)
    server_name=sys.argv[1]
    port_number=sys.argv[2]
    if not port_number.isdigit():
        print("Error: Invalid Port Number")
        sys.exit(1)        
    load_model()
    app.run(server_name, threaded=False, port=int(port_number),debug=False)

if __name__ == '__main__':
    main()
