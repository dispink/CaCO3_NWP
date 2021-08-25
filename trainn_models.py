import numpy as np 
import pandas as pd
from nwp_cali import PrepareData
from sklearn.model_selection import train_test_split
from sklearn.decomposition import NMF
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from joblib import dump

import datetime
date = datetime.datetime.now().strftime('%Y%m%d')

from time import perf_counter
path = '/home/users/aslee/CaCO3_NWP/'
y_tuple = {}

measurement = 'CaCO3%'
print('Begin NMF+SVR: {}'.format(measurement))
start = perf_counter()
prepare = PrepareData(measurement=measurement)
X, y = prepare.produce_Xy(prepare.select_data())
X_train, X_dev, y_train, y_dev = train_test_split(
    X, y, test_size = 0.2, shuffle = True, random_state = 24)

# specified to the measurement
# the max_iter is increased from 8000 to 10000 to avoid faled convergence
pipe = make_pipeline(NMF(n_components=4, max_iter=10000, random_state=24), 
                     SVR(C=1e2, gamma=1e3))
pipe.fit(X_train, np.log(y_train))

dump(pipe, 
     '{}models/{}_nmf+svr_model_{}.joblib'.format(
         path, measurement[:-1].lower(), date)) 
print("The computation takes {} mins.".format(
    (perf_counter() - start)/60))

y_df = pd.DataFrame([y_dev, np.exp(pipe.predict(X_dev))], index=[measurement, '{}_pred'.format(measurement)]).T

######################## Change measurement ###########################

measurement = 'TOC%'
print('Begin NMF+SVR: {}'.format(measurement))
start = perf_counter()
prepare = PrepareData(measurement=measurement)
X, y = prepare.produce_Xy(prepare.select_data())
X_train, X_dev, y_train, y_dev = train_test_split(
    X, y, test_size = 0.2, shuffle = True, random_state = 24)

# specified to the measurement
pipe = make_pipeline(NMF(n_components=13, max_iter=8000, random_state=24), 
                     SVR(C=10, gamma=1e3))
pipe.fit(X_train, np.log(y_train))

dump(pipe, 
     '{}models/{}_nmf+svr_model_{}.joblib'.format(
         path, measurement[:-1].lower(), date)) 
print("The computation takes {} mins.".format(
    (perf_counter() - start)/60))

tmp_df = pd.DataFrame([y_dev, np.exp(pipe.predict(X_dev))], index=[measurement, '{}_pred'.format(measurement)]).T

pd.concat([y_df, tmp_df], axis=1, join='outer').to_csv('results/y_dev_preds_{}.csv'.format(date))