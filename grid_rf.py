import sys
import numpy as np 
import pandas as pd
from nwp_cali import PrepareData
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import NMF
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

import datetime
date = datetime.datetime.now().strftime('%Y%m%d')

from time import perf_counter
path = '/home/users/aslee/CaCO3_NWP/'

measurement = sys.argv[1]
start = perf_counter()

prepare = PrepareData(measurement=measurement)
X, y = prepare.produce_Xy(prepare.select_data())
X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size = 0.2, shuffle = True, random_state = 24)

print('Begin NMF+RF: {}'.format(measurement))

pipe = Pipeline([('nmf', NMF(max_iter = 8000, random_state = 24)), 
                 ('rf', RandomForestRegressor(random_state = 24))])

params = {
    'nmf__n_components': range(5, 11),
    'rf__n_estimators': [100, 1000, 10000],
    'rf__max_depth': [5, 10, 20, 30]
}

grid = GridSearchCV(pipe, param_grid = params, cv = 10, n_jobs = -1)  

grid.fit(X_train, np.log(y_train))

print('The best cv score: {:.3f}'.format(grid.best_score_)) 
print('The best model\'s parameters: {}'.format(grid.best_estimator_))

pd.DataFrame(grid.cv_results_).to_csv('{}results/{}_grid_nmf+rf_{}.csv'.format(path, measurement[:-1].lower(), date))

from joblib import dump
dump(grid.best_estimator_, '{}models/{}_nmf+rf_model_{}.joblib'.format(path, measurement[:-1].lower(), date)) 

print("The computation takes {} hours.".format((perf_counter() - start)/3600))