import numpy as np 
import pandas as pd
from nwp_cali import PrepareData
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import NMF
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline

import datetime
date = datetime.datetime.now().strftime('%Y%m%d')

from time import perf_counter
path = '/home/users/aslee/CaCO3_NWP/'
for measurement in ['CaCO3%', 'TOC%']:
    start = perf_counter()

    prepare = PrepareData(measurement=measurement)
    X, y = prepare.produce_Xy(prepare.select_data())
    X_train, X_dev, y_train, y_dev = train_test_split(X, y, test_size = 0.2, shuffle = True, random_state = 24)

    print('Begin NMF+SVR: {}'.format(measurement))

    pipe = make_pipeline(NMF(max_iter = 8000, random_state = 24), SVR())
    params = {
        'nmf__n_components': range(5, 11),
        'svr__C': np.logspace(2, 8, 7),
        'svr__gamma': np.logspace(-4, 2, 7)
    }
    grid = GridSearchCV(pipe, param_grid = params, cv = 10, n_jobs = -1)  

    grid.fit(X_train, np.log(y_train))

    print('The best cv score: {:.3f}'.format(grid.best_score_)) 
    print('The best model\'s parameters: {}'.format(grid.best_estimator_))

    pd.DataFrame(grid.cv_results_).to_csv('{}results/caco3_grid_nmf+svr_{}.csv'.format(path, date))

    from joblib import dump, load
    dump(grid.best_estimator_, '{}models/caco3_nmf+svr_model_{}.joblib'.format(path, date)) 

    print("The computation takes {} hours.".format((perf_counter() - start)/3600))