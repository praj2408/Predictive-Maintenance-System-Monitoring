import os
import sys

from src.Predictive_Maintainance.logger import logging
from src.Predictive_Maintainance.exception import CustomException

import pandas as pd
import numpy as np

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

from imblearn.over_sampling import SMOTE

from src.Predictive_Maintainance.utils.utils import type_of_failure

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
            df.apply(lambda row: type_of_failure(row.name,df), axis=1)
            df['type_of_failure'].replace(np.NaN, 'no failure', inplace=True)
            
            #drop productid and uid
            df.drop(['UDI', 'Product ID'], axis=1, inplace=True)

            
            #convert kalvin to celcius
            df['Air temperature [c]'] = df['Air temperature [K]'] - 273.15
            df['Process temperature [c]'] = df['Process temperature [K]'] - 273.15
            df.drop(['Air temperature [K]', 'Process temperature [K]'], axis=1, inplace=True)
            
            
            # categorical Encoding
            df['Type'] = ordinal_encoder.fit_transform(df[['Type']])

            
            # lable encoding
            df['type_of_failure'] = label_encoder.fit_transform(df['type_of_failure'])

            # feature scaling
            scaled_data = scaler.fit_transform(df)
            
            scaled_data_df = pd.DataFrame(scaled_data, columns=df.columns)


            # oversampling
            
    
            scaled_data_df.to_csv(self.data_transformation_config.preprocessor_csv_file_path, index=False)
            
            
            return scaled_data_df
        
        except Exception as e:
            logging.info("Error occured during DataTransformation stage")
            raise CustomException(e, sys)