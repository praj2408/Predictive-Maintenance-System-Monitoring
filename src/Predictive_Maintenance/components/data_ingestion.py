import os
import sys

from src.Predictive_Maintenance.logger import logging
from src.Predictive_Maintenance.exception import CustomException

import pandas as pd
import numpy as np


class DataIngestionConfig:
    raw_data_path:str = os.path.join("artifacts", "raw.csv")
    
    
    
class DataIngestion:
    
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        
        try:
            
            data = pd.read_csv(os.path.join("notebooks","data","data.csv"))
            logging.info("Reading the dataset Completed")
            
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Saved the raw dataset in artifacts directory")
            
            #print(data.head())
            
            
            return self.ingestion_config.raw_data_path
    
        except Exception as e:
            logging.info("Exception during occured at data ingestion stage")
            raise CustomException(e, sys)