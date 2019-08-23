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

import csv

X = []
y = []

with open('transaction_20kln.csv', 'r') as f:
    reader = csv.reader(f)
    for example in reader:

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
        # 501   DOUBLE                    8  RISK_RATING                              12
        x.append(float(example[12]))
        # 449   VARCHAR                 100  INCOME_BAND                              11
        x.append(example[13])
        # 497   INTEGER                   4  CREDIT_LIMIT                             12
        x.append(int(example[14]))
        # 453   CHARACTER                 1  FLAG                                      4

        print(example[15])
        if(example[15] is 'R'):
            flag = 1
        else:
            flag = 0
        # 393   TIMESTAMP                26  TRANS_TIMESTAMP                          15
        # 497   INTEGER                   4  YEAR                                      4
        # 497   INTEGER                   4  MONTH                                     5
        # 497   INTEGER                   4  DAY                                       3

        X.append(x)
        y.append(flag)


import time

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=43)

print(X_test[0])

import sklearn
print(sklearn.__version__)

from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(categories='auto',handle_unknown='ignore')
# enc = OneHotEncoder(handle_unknown='ignore')
X_train = enc.fit_transform(X_train)
X_test = enc.transform(X_test)

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()

clf.fit(X_train, y_train)

# probability of a risky transaction
z = clf.predict_proba(X_test)[:,1]

from sklearn.metrics import average_precision_score
print("Average prec. score: %f" % (average_precision_score(y_test, z)))


import numpy as np
model = np.hstack((clf.intercept_, clf.coef_[0]))
np.save('risk_model.npy', model)

for i in range(0,10):
    prob = 1.0/(1.0+np.exp(-model[0]-X_test[i].dot(model[1:])))
    assert(prob == z[i])


import pickle
pickle.dump( enc, open('risk_encoder.p','wb'))


