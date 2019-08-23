Model Building and Deployment (on Power Little-endian Linux)

Linux version supported is RHEL 7.6

train.py - Python code to run training on the data (in cust_history.csv) and save the Tensorflow model

cust_history.csv - Training data in csv format

flask-linux-server.py - Python script to load the TensorFlow model and export REST APIs to access the model

process_data.py - Helper script to read the data.

Model Training
---------------
To train and generate Tensorflow  model 

$ python train.py

The output of this script will save model in H5 format in file called cc_risk_analysis_model.h5 
and the transformed data is saved as feature_transofmed_model.pkl

Model Deployment
-----------------

To export REST APIs via flask-based server on Linux LPAR

$ python flask-linux-server.py <your hostname> <portno>
  
This command starts a flask-based server and exposes REST APIs to access the model.




