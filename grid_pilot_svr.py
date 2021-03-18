import numpy as np 
import pandas as pd

import datetime
date = datetime.datetime.now().strftime('%Y%m%d')

from time import perf_counter
start = perf_counter()

path = '/home/users/aslee/CaCO3_NWP/'

from sklearn.model_selection import train_test_split

data_df = pd.read_csv('{}data/spe+bulk_SO264-15-2.csv'.format(path))

X = data_df.iloc[:, 1: -5].values
X = X / X.sum(axis = 1, keepdims = True)
y = data_df.caco3_percent.values


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import NMF
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV


print('Begin: Pilot SVR')

pipe = Pipeline([('scaling', StandardScaler()),('preprocessing', PCA()), ('svr', SVR())])

param_grid = [
    {'scaling': [StandardScaler()],
     'preprocessing': [PCA(n_components=5, whiten=True)],
     'svr__C': np.logspace(-3, 5, 9),
     'svr__gamma': np.logspace(-5, 3, 9)},
    {'scaling': [None],
     'preprocessing': [NMF(n_components=5, random_state=24, max_iter=4000)],
     'svr__C': np.logspace(-3, 5, 9),
     'svr__gamma': np.logspace(-5, 3, 9)}
]

grid = GridSearchCV(pipe, param_grid = param_grid, cv = 5, n_jobs = -1, return_train_score = False)  

grid.fit(X, y)

print('The best cv score: {:.3f}'.format(grid.best_score_)) 
print('The best model\'s parameters: {}'.format(grid.best_estimator_))

pd.DataFrame(grid.cv_results_).to_csv('{}results/pilot_grid_svr_{}.csv'.format(path, date))

print("The computation takes {} hours.".format((perf_counter() - start)/3600))