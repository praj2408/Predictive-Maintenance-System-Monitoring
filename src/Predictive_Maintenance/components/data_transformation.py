import os
import sys
from pathlib import Path

import pickle

from src.Predictive_Maintenance.logger import logging
from src.Predictive_Maintenance.exception import CustomException

import pandas as pd
import numpy as np

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

from imblearn.over_sampling import SMOTE

from src.Predictive_Maintenance.utils.utils import type_of_failure

ordinal_encoder =OrdinalEncoder(categories=[['L', 'M', 'H']])
label_encoder = LabelEncoder()
scaler = MinMaxScaler()





class DataTransformationConfig:
    preprocessor_csv_file_path: str = os.path.join("artifacts", "preprocessed_csv.csv")
    
    

class DataTransformation:
    
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def initiate_data_transformation(self, raw_data_path):
        
        try:
        
            df = pd.read_csv(raw_data_path)
            logging.info("read data complete")
            logging.info(f"df dataframe head: \n {df.head().to_string()}")
        
            # create type of failure column
            logging.info("create 'type of failure' column")
            df.apply(lambda row: type_of_failure(row.name, df), axis=1)
            logging.info("create 'type of failure' column completed successfully")
            #df['type_of_failure'].replace(np.NaN, 'no failure', inplace=True)
            
            #drop productid and uid
            
            df.drop(['UDI', 'Product ID'], axis=1, inplace=True)
            df.drop(['TWF', 'HDF', 'PWF', 'OSF', 'RNF'], axis=1, inplace=True)
            logging.info('removed productid and uid from the dataset')

            
            #convert kalvin to celcius
            logging.info('converting kelvin to celcius')
            df['Air temperature [c]'] = df['Air temperature [K]'] - 273.15
            df['Process temperature [c]'] = df['Process temperature [K]'] - 273.15
            df.drop(['Air temperature [K]', 'Process temperature [K]'], axis=1, inplace=True)
            
            logging.info('converted kelvin to celcius successfully')

            
            
            # categorical Encoding
            df['Type'] = ordinal_encoder.fit_transform(df[['Type']])

            
            # lable encoding
            df['type_of_failure'] = label_encoder.fit_transform(df['type_of_failure'])
            
            logging.info('Encoding completed successfully')

            # feature scaling
            scale_cols = ['Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Air temperature [c]', 'Process temperature [c]']
            
            df_scaled = scaler.fit_transform(df[scale_cols])
            
            with open(Path("artifacts", "scaler.pkl"), "wb") as f:
                pickle.dump(scaler, f)
            
            
            df_scaled = pd.DataFrame(df_scaled)
            df_scaled.columns = scale_cols

            df.drop(scale_cols, axis=1, inplace=True)

            df_scaled = pd.concat([df, df_scaled], axis=1)
            
            logging.info("data scaling stage completed successfully")
            
        
            # oversampling
            logging.info("Oversampling stage begin.............")
            smote = SMOTE(sampling_strategy='auto')
            
            X = df_scaled.drop('type_of_failure', axis=1)
            y = df_scaled['type_of_failure']

            X_resampled, y_resampled = smote.fit_resample(X, y)

            df_sampled = pd.concat([X_resampled, y_resampled], axis=1)
            
            logging.info(f"df sampled head: \n {df_sampled.head().to_string()}")
            
            logging.info("Over sampling stage completed successfully")
                
            df_sampled.to_csv(self.data_transformation_config.preprocessor_csv_file_path, index=False)
            
            
            return df_sampled
        
        except Exception as e:
            logging.info("Error occured during DataTransformation stage")
            raise CustomException(e, sys)