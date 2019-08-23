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
import numpy as np
import pickle
import sklearn
print(sklearn.__version__)

class RiskPredictor:
    """ Risk predictor

        Args:

        Attributes:
            encoder (sklearn.preprocessing.OneHostEncoder): one-hot encoder
            model (np.array): pre-trained logistic model from SnapML
    """

    PRED_STATUS = {'NOT_INITIALIZED':0, 'READY_FOR_WORK':1, 'BUSY':2, 'ERROR':3}
    status = PRED_STATUS['NOT_INITIALIZED']
    def __init__(self):
 
        self.status = self.PRED_STATUS['NOT_INITIALIZED']

        # Read pre-trained one-hot encoder
        self.enc = pickle.load(open('./model/risk_encoder.p', 'rb'))

        # Read pre-trained model 
        self.model = np.load("./model/risk_model.npy")

        self.status = self.PRED_STATUS['READY_FOR_WORK']

    def predict(self, example):
        """ Predict probability of click given feature vector
        Args:
            example (list): feature vector

        Returns:
            float: Probability of click
        """

        # The READY and BUSY status is set at the riskpredictor level
        vec = self.vectorize(example)

        prob = 1.0/(1.0+np.exp(-self.model[0]-vec.dot(self.model[1:])))

        return prob[0]


    def vectorize(self, example):
        """ Vectorize an example feature vector string
        Args:
            example (list): raw feature vector

        Returns:
           list: sparse encoder feature vector
        """
        x = []
        # 493   BIGINT                    8  TRANS_ID                                  8
        x.append(int(example[0]))
        # 493   BIGINT                    8  PRODUCT_ID                               10
        x.append(int(example[1]))
        # 497   INTEGER                   4  LINE_NUMBER                              11
        x.append(int(example[2]))
        # 497   INTEGER                   4  QUANTITY                                  8
        x.append(int(example[3]))
        # 481   DOUBLE                    8  PRICE                                     5
        x.append(float(example[4]))
        # 481   DOUBLE                    8  TAX                                       3
        x.append(float(example[5]))
        # 493   BIGINT                    8  CUSTOMER_ID                              11
        x.append(int(example[6]))
        # 493   BIGINT                    8  MFR_ID                                    6
        x.append(int(example[7]))
        # 449   VARCHAR                  50  PROD_NAME                                 9
        x.append(example[8])
        # 501   SMALLINT                  2  PROD_CATEGORY                            13
        x.append(int(example[9]))
        # 449   VARCHAR                  10  PROD_SIZE                                 9
        x.append(example[10])
        # 481   DOUBLE                    8  RETAIL_PRICE                             12
        x.append(float(example[11]))
        # 501   SMALLINT                  2  RISK_RATING                              11
        x.append(float(example[12]))
        # 449   VARCHAR                 100  INCOME_BAND                              11
        x.append(example[13])
        # 497   INTEGER                   4  CREDIT_LIMIT                             12
        x.append(int(example[14]))

        return self.enc.transform([x])

