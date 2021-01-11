import numpy as np 
import pandas as pd

import datetime
date = datetime.datetime.now().strftime('%Y%m%d')

from time import perf_counter
start = perf_counter()

path = '/home/users/aslee/CaCO3_NWP/'

from sklearn.model_selection import train_test_split

data_df = pd.read_csv('{}data/spe+bulk_dataset_20201215.csv'.format(path))
# All data points contain TOC
X = data_df.iloc[:, 1: -5].values
X = X / X.sum(axis = 1, keepdims = True)
y = data_df['TOC%'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, shuffle = True, random_state = 24)

print('Begin: TOC')

from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import NMF
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline

pipe = make_pipeline(NMF(max_iter = 8000, random_state = 24), SVR())
params = {
    'nmf__n_components': range(5, 12),
    'svr__C': np.logspace(1, 8, 8),
    'svr__gamma': np.logspace(-4, 2, 7)
}
grid = GridSearchCV(pipe, param_grid = params, cv = 10, n_jobs = -1, return_train_score = False)  

grid.fit(X_train, np.log(y_train))

print('The best cv score: {:.3f}'.format(grid.best_score_)) 
print('The best model\'s parameters: {}'.format(grid.best_estimator_))

pd.DataFrame(grid.cv_results_).to_csv('{}results/toc_grid_nmf+svr_{}.csv'.format(path, date))

from joblib import dump, load
dump(grid.best_estimator_, '{}models/toc_nmf+svr_model_{}.joblib'.format(path, date)) 

print("The computation takes {} hours.".format((perf_counter() - start)/3600))