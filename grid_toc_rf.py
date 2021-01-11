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

print('Begin: TOC-RF')

from sklearn.decomposition import NMF
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline

score_train = []
score_test = []
depthS = []
estimatorsS = []

for depth in [5, 10, 20, 35, 50]:
    for n_estimators in [100, 1000, 10000]:
        rf = make_pipeline(NMF(n_components=9, max_iter = 8000, random_state = 24), 
                             RandomForestRegressor(n_estimators=n_estimators, max_depth= depth, n_jobs=-1, random_state=24))
        rf.fit(X_train, np.log(y_train))
        score_train.append(rf.score(X_train, np.log(y_train)))
        score_test.append(rf.score(X_test, np.log(y_test)))
        depthS.append(depth)
        estimatorsS.append(n_estimators)
        
pd.DataFrame({'n_estimators': estimatorsS,
              'max_depth': depthS,
              'score_train': score_train,
              'score_test': score_test
             }).to_csv('{}results/toc_grid_nmf+rf_{}.csv'.format(path, date))

print("The computation takes {} hours.".format((perf_counter() - start)/3600))