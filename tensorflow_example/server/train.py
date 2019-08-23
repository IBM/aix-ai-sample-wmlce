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

#This script has to be run on RHEL POWER VM Linux system
#This script creates a keras model using customer history data and saves the model

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Dropout
from tensorflow.python.keras import optimizers
from sklearn.model_selection import train_test_split
from process_data import read_customer_history
from sklearn.externals import joblib

def build_model():
    model = Sequential()

    model.add(Dense(units=200,
                input_dim=25,
                #keprnel_initializer='uniform',
                activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(units=200,
                #kernel_initializer='uniform',
                activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(units=1,
                #kernel_initializer='uniform',
                activation='sigmoid'))

    optimizer = optimizers.Adam(lr=0.001)

    model.compile(loss='binary_crossentropy',
              optimizer=optimizer, metrics=['accuracy'])

    return model

features,label,le,min_max_scalar = read_customer_history()
train_feature,test_feature,train_label,test_label = \
	train_test_split(features, label, test_size=0.3, random_state=42, stratify=label)

print ('train feature shape = {train_feature.shape} label = {train_label.shape} ',  
	'test feature shape = {test_feature.shape} label shape = {test_label.shape}')

model = build_model()
print(model.summary())

train_history = model.fit(x=train_feature, y=train_label, validation_split=1,
	epochs=500, batch_size=100, verbose=2)

scores = model.evaluate(train_feature, train_label); print('train accuracy=',scores[1])
scores = model.evaluate(test_feature, test_label); print('test accuracy=',scores[1])

#for i in features:
#	print i
#	p = model.predict_classes(i.reshape(1,25))
#	print p

joblib.dump((le,min_max_scalar),'feature_transform_model.pkl')
model.save('cc_risk_analysis_model.h5')
print('model saved to disk')
