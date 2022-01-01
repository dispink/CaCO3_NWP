# CaCO3_NWP

It is a cooperative project with JC aiming to build models for predicting CaCO<sub>3</sub>, TOC, and TC using spectra produced by Avaatech.
The model is training by the bulk measurements (low resolution: several centimeters to meters) and the spectra (high resolution: 1 cm) provided by JC. These data are measured from the sediment cores taken at spreading over the high latitude Northwest Pacific (37°N-52°N) and Pacific sector of the Southern Ocean (53°S-63°S), with a water depth coverage from 1211 m to 4853 m deep. 

## Workflow
### Pilot test
`pilot_test.ipynb` gives the fundation of how to prepare data and what combination of machine learning (ML) algorithms will we use. The core SO264-15-2 is taken as the trial data. Its promising result let us decide to dive into this project.

### Build models: include whole SO264
1. We include the whole cores of the cruise SO264. The database is built using `build_database_01.ipynb`, `build_database_02.ipynb`, `build_database_03.ipynb` and `build_database_04.ipynb`. 
1. The models are built and improved by `build_models_01.ipynb`, `build_models_02.ipynb` and `build_models_03.ipynb`. We start to use the mean absolute errir and the max. residual to evaluate the prediction performance besides R<sup>2<sup> since we find out the statiscal problem of TOC. 
1. These models are applied to predict bulk chemistry measurements of those sediments only having XRF data but no bulk chemistry measurements by `prediction_01.ipynb`.
1. We find a trick to prevent the prediction of negative bulk chemistry values by making logrithm. Therefore, the models are rebuilts (`build_models_04.ipynb`, `build_models_04.ipynb`, `build_models_06.ipynb`). The predictions are redo via `prediction_02.ipynb`.

Detail output files please check ths log in Git.
