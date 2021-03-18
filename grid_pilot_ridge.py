import numpy as np 
import pandas as pd

import datetime
date = datetime.datetime.now().strftime('%Y%m%d')

from time import perf_counter
start = perf_counter()

path = '/home/users/aslee/CaCO3_NWP/'

data_df = pd.read_csv('{}data/spe+bulk_SO264-15-2.csv'.format(path))

X = data_df.iloc[:, 1: -5].values
X = X / X.sum(axis = 1, keepdims = True)
y = data_df.caco3_percent.values

print('Begin: Pilot Ridge')

from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline

pipe = make_pipeline(StandardScaler(), PCA(n_components=5, whiten=True), Ridge())
params = {'ridge__alpha': np.logspace(-8, 1, 10)}

grid = GridSearchCV(pipe, param_grid = params, cv = 5, n_jobs = -1, return_train_score = False)  

grid.fit(X, y)

print('The best cv score: {:.3f}'.format(grid.best_score_)) 
print('The best model\'s parameters: {}'.format(grid.best_estimator_))

pd.DataFrame(grid.cv_results_).to_csv('{}results/pilot_grid_pca+ridge_{}.csv'.format(path, date))

print("The computation takes {} hours.".format((perf_counter() - start)/3600))