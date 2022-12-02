# CaCO3_NWP
It is a cooperative project with JC aiming to build models for predicting CaCO<sub>3</sub>, TOC, and TC using spectra produced by Avaatech.
The model is training by the bulk measurements (low resolution: several centimeters to meters) and the spectra (high resolution: 1 cm) provided by JC. These data are measured from the sediment cores taken at spreading over the high latitude Northwest Pacific (37°N-52°N) and Pacific sector of the Southern Ocean (53°S-63°S), with a water depth coverage from 1211 m to 4853 m deep. 

## Publication
Lee, AS., Chao, WS., Liou, S.Y.H. et al. Quantifying calcium carbonate and organic carbon content in marine sediments from XRF-scanning spectra with a machine learning approach. Sci Rep 12, 20860 (2022). https://doi.org/10.1038/s41598-022-25377-x

## Workflow
### Pilot test
`pilot_test.ipynb` `grid_pilot_ridge.py`, `grid_pilot_svr.py` and `submit_pilot.sh` give the fundation of how to prepare data and what combination of machine learning (ML) algorithms (Principal componemt analysis, Non-negative matrix factorization, Ridged regression, Support vector regression, Randomforest) will we use. The core SO264-15-2 is taken as the trial data. The promising outcome let us decide to dive into this project.

### Build models: include whole SO264
1. We include the whole cores of the cruise SO264. The database is built using `build_database_01.ipynb`, `build_database_02.ipynb`, `build_database_03.ipynb` and `build_database_04.ipynb`. 
1. The models are built and improved by `build_models_01.ipynb`, `build_models_02.ipynb` and `build_models_03.ipynb`. We start to use the mean absolute errir and the max. residual to evaluate the prediction performance besides R<sup>2<sup> since we find out the statiscal problem of TOC. 
1. These models are applied to predict bulk chemistry measurements of those sediments only having XRF data but no bulk chemistry measurements by `prediction_01.ipynb`.
1. We find a trick to prevent the prediction of negative bulk chemistry values by making logrithm. Therefore, the models are rebuilts (`build_models_04.ipynb`, `build_models_04.ipynb`, `build_models_06.ipynb`). The predictions are redo via `prediction_02.ipynb`.
1. Visualize spectrum and data distribution (`quick_analysis.ipynb`).

### Build models: include cores (LV28-44-3, LV29-114-3, SO178-12-3)
This an update after discuss with JC and Dr. Lembke-Jene. He provide more cores to increase TOC measurement ranges.
1. Update database (`build_database_05.ipynb`).
1. Rebuild models (`grid_caco3.py`, `grid_toc.py`, `grid_toc_rf.py`, `submit_svr.sh`, `submit_rf.sh`) and make new predictions (`prediction_03.ipynb`).
1. Visulize the gridsearch and models' performance. Also the data histograms are produced (`build_models_07.ipynb`).
1. Polish the figures of our results, which fits to the logic of writing paper at this step(`plot_for_paper_01.ipynb`).
1. The latest CaCO<sub>3<sub> model is evaluated on the core PS75-056-1. The prediction isn't very well.
1. We realize the XRF scanner's scanning head was changed once. The spectra are different in the same core but different heads. In order to be sure, we check scanning information of the cores (`test_heads.ipynb`).

### Build models: reselect cores
Since we realize the effect of changing scanning head, we polish our database to have those cores using the same scanning head. Several new cores are added (also triger cores) after discussing with JC and Dr. Lembke-Jene. We decide to focus on Calcium Carbonate and TOC only.
1. Update database (`build_database_05.ipynb`, `build_database_06.ipynb`). The spe+bulk data amount increases notibly (802 -> 2330).
1. Find optimal parameters and rebuild models (`grid_svr.py`, `submit_svr.sh`, `trainn_models.py`). I develop `nwp_cali.py` to include functions to prepare data. The proceedures and results are recorded in `build_models_08.ipynb`, `build_models_09.ipynb`.
1. Due to my curiosity, I quickly tried the Ridge regression and Randomforest to build models (`grid_lr.py`, `grid_rf.py`, `submit_lr.sh`, `submit_rf.sh`) without fine-tuning parameters.
1. Include SO202-37-2_rescan to the database (`build_database_06.ipynb`). It's the core scanned by the old head but now we try it on the new head. We hope this core (NW-Pacific) can be used as casestudies along with the other core (SE-Pacific) to evaluate and discuss our models' performance (`build_models_09.ipynb`). The models are, hence, evaluated both in the test set, which is split from the training set in the begining, and the casestudy cores. The spe+bulk data amount increases (2330 -> 2350).
1. After discussing with JC, we decide to waive out the core SO202-37-2_rescan because the scanning head was a bit problemetic during the core's scan. Hence, we'll focus on the evaluation of the test set and PS75-056-1 as the casestudy.
1. Include the 95% confidence interval to estimate our models' uncertainty (`build_database_10.ipynb`). The estimation uses t-distribution based on the performance on the test set.

### Include more cores to the casestudy
Add two more cores from the Northwest Pacific (SO264-69-2 and LV28-44-3) with the existing core from the South Pacific sector (PS75-056-1). The upper part of LV28-44-3 was included to our database but not used due to the inconsistent scanning setting. This time we include the data of the lower part of LV28-44-3, scanned by the same setting as other cores.
1. Update database (`build_database_07.ipynb`). The spe+bulk data amount increases (2350 -> 2643).
1. Evaluate the performance of the latest models on these new casestudy cores (`build_models_11.ipynb`). A new confidence interval was calculated by including the casestudy cores. The generalization of our TOC model to cores outside of our database is confirmed to be crippled while the CaCO3 model stays excellent. The performance of these two models in our own database are still outstanding. The high-resolution of bulk chemistry quantifications are done by `prediction_05.ipynb`.

### Prepare for application
1. Plots for paper are prepared in the series of `plot_for_paper_XX.ipynb`.
1. Demonstration of applying our models is prepared in `demo.ipynb`. The new `class()` for quantification is added to `nwp_cali.py`.

P.S. Detail output files please check ths log in Git.<br>
P.S. "dev set" and "test set" stand for the same meaning of data subsets in the workflow. I was planning to have different data subsets for them, but at the end I don't think it's necessary.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. If you're a newby student want to work on large geochemical dataset, you might find something interesting in this project. Any application or modification based on this repository, please kindly cite the direct publication mentioned above.
