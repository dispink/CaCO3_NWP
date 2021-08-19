import pandas as pd
import numpy as np

class PrepareData:
    """
    This is a class gathering the functions to prepare data. Be careful,
    the using of measurement (CaCO3%, TC%, TOC%) data need to follow the 
    selected measurment in the initialization because the filtering is
    based that selection only. 
    """

    def __init__(self, measurement,
                 data_dir='~/CaCO3_NWP/data/spe+bulk_dataset_20210818.csv', 
                 select_dir='~/CaCO3_NWP/data/ML station list.xlsx',
                 channel_amount=2048):
        while True:
            if measurement not in ['CaCO3%', 'TC%', 'TOC%']:        
                print('The measurement should be strings of CaCO3%, TC% or TOC%.')
                break
            else:
                self.measurement = measurement
            self.data_dir = data_dir
            self.select_dir = select_dir
            self.channel_amount=channel_amount
            break

    def select_data(self):
        """
        This function is to select the chosen cores in the file 
        (select_dir) and having the measurement (CaCO3, TC, TOC) from a 
        pd.DataFrame (data_dir). This dataset has composite_id, 
        channels, TC%, TOC%, CaCO3%, core, mid_depth_mm and the output
        will be in the same format. The negative measurement values are
        excluded.
        """
        data_df = pd.read_csv(self.data_dir)
        xl_df = pd.read_excel(self.select_dir, sheet_name='CHOSEN')
        mask = ((data_df.core.isin(xl_df.Station)) & 
                (~data_df[self.measurement].isna()) &
                (data_df[self.measurement] >= 0))
        return data_df.loc[mask, :]

    def produce_Xy(self, data_df):
        """
        This function takes the input pd.DataFrame, usually the output 
        of self.select_data (the data shouldn't have NAs and negative 
        value), to generate X (channels normalized by the row sum) and
        y (weight percent, the 0 values are replaced by 0.01). The 
        ouputs are in np.ndarray
        """
        X = data_df.iloc[:, 1: -5].values
        X = X / X.sum(axis = 1, keepdims = True)
        y = data_df[self.measurement].replace(0, 0.01).values

        return X, y

if __name__ == '__main__':
    prepare = PrepareData(measurement='CaCO3%')
    X, y = prepare.produce_Xy(prepare.select_data())
    print(len(X))

